from __future__ import annotations
import json
import re
import difflib
from typing import List, Dict, Optional
from app.core.config import settings
import numpy as np
from sqlalchemy.orm import Session
from app.models.mapping import SemanticFieldMappingModel
from app.crud.mapping_crud import bulk_create_semantic_field_mappings

from sentence_transformers import SentenceTransformer

# Optional Redis cache
redis_client = None
REDIS_URL = settings.REDIS_URL
if REDIS_URL:
    try:
        import redis

        redis_client = redis.from_url(REDIS_URL)
    except Exception:
        redis_client = None

# Sentence Transformers (free, open-source embeddings)
RULE_BASED_MAPPING_ENABLED = settings.RULE_BASED_MAPPING_ENABLED
USE_SEMANTIC_EMBEDDINGS = getattr(settings, "USE_SEMANTIC_EMBEDDINGS", True)
embedding_model = True
try:
    from sentence_transformers import SentenceTransformer

    # Lightweight model: 22MB, very fast, works on CPU
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    embedding_model = None


def _cache_get(key: str) -> List | Dict | None:
    if not redis_client:
        return None
    raw = redis_client.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def _cache_set(key: str, value: List[float] | Dict, ttl: int = 86400) -> None:
    if not redis_client:
        return
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception:
        pass


def _embedding(text: str) -> List[float]:
    """Get embedding for text using Sentence Transformers.

    Falls back to difflib-based matching if model unavailable.
    Caches results in Redis if available.
    """
    key = f"emb:{text.lower()}"
    cached = _cache_get(key)

    if cached:
        return cached

    if embedding_model and USE_SEMANTIC_EMBEDDINGS:
        # Using Sentence Transformers (free, CPU-friendly)
        emb = embedding_model.encode(text).tolist()
    else:
        # Fallback: character frequency vector (very rough)
        vec = np.zeros(128, dtype=float)
        for ch in text.lower():
            if 0 <= ord(ch) < 128:
                vec[ord(ch)] += 1.0
        norm = np.linalg.norm(vec) or 1.0
        emb = (vec / norm).tolist()

    _cache_set(key, emb)
    return emb


def _cosine(a: List[float], b: List[float]) -> float:
    """Cosine similarity between two vectors."""
    va, vb = np.array(a), np.array(b)
    denom = (np.linalg.norm(va) * np.linalg.norm(vb)) or 1.0
    return float(np.dot(va, vb) / denom)


def suggest_mapping(ngo_fields: List[str], donor_fields: List[str]) -> List[Dict]:
    """
    Returns [{ngo_field, donor_field, confidence}] using Sentence Transformers
    embeddings, with fallback to difflib.

    Uses cosine similarity for matching with semantic embeddings.
    """
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    if not donor_fields:
        return []

    # If embeddings unavailable, use difflib
    if not embedding_model or not USE_SEMANTIC_EMBEDDINGS:
        suggestions: List[Dict] = []
        for nf in ngo_fields:
            match = difflib.get_close_matches(nf, donor_fields, n=1, cutoff=0.0)
            best = match[0] if match else donor_fields[0]
            conf = difflib.SequenceMatcher(a=nf.lower(), b=best.lower()).ratio()
            suggestions.append({"ngo_field": nf, "donor_field": best, "confidence": round(conf, 3)})
        return suggestions

    # With Sentence Transformers embeddings
    donor_vecs = {df: _embedding(df) for df in donor_fields}
    out: List[Dict] = []
    for nf in ngo_fields:
        nf_vec = _embedding(nf)
        best_field, best_score = donor_fields[0], -1.0
        for df, dv in donor_vecs.items():
            score = _cosine(nf_vec, dv)
            if score > best_score:
                best_field, best_score = df, score
        # Normalize score to 0-1 range (cosine can be negative)
        confidence = max(0.0, min(1.0, (best_score + 1.0) / 2.0))
        out.append({"ngo_field": nf, "donor_field": best_field, "confidence": round(confidence, 3)})
    return out


SEMANTIC_TARGETS = {
    "budget_category",
    "budget_field",
    "extra_field",
    "header_metadata",
    "currency",
    "date_range",
    "person",
    "ignored",
}


CANONICAL_KEYS = {
    "organisation_name",
    "project_name",
    "project_reference",
    "project_period",
    "currency",
    "budget_category",
    "contact_person",
}


def normalize_value(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[\"']", "", value)
    return value


CURRENCY_CODES = {"eur", "usd", "gbp", "nok"}

CATEGORY_KEYWORDS = {
    "staff": "staff_costs",
    "office": "office_costs",
    "equipment": "equipment",
    "travel": "travel",
}

HEADER_KEYWORDS = [
    "budget summary",
    "detailed budget",
    "authorised signatory",
]

FIELD_PATTERNS = {
    "project name": "project_name",
    "organisation name": "organisation_name",
    "project ref": "project_reference",
    "project period": "project_period",
    "contact person": "contact_person",
}


def rule_based_suggestion(value: str):
    v = normalize_value(value)

    if v in CURRENCY_CODES:
        return ("currency", "currency", 0.99)

    for h in HEADER_KEYWORDS:
        if h in v:
            return ("header_metadata", None, 0.95)

    for k, canonical in FIELD_PATTERNS.items():
        if k in v:
            return ("budget_field", canonical, 0.96)

    for k, canonical in CATEGORY_KEYWORDS.items():
        if k in v:
            return ("budget_category", canonical, 0.94)

    return None


def suggest_semantic_mapping(values: List[str], db: Session, valid_user: Dict) -> Dict:
    """
    Suggest semantic mappings using rule-based heuristics.
    Returns [{ngo_field, mapped_to, mapped_key, confidence}]
    """
    suggestions: List[Dict] = []
    unknown: List[Dict] = []
    for raw in values:
        normalized = normalize_value(raw)
        if RULE_BASED_MAPPING_ENABLED:
            rule_suggestion = rule_based_suggestion(normalized)
            if rule_suggestion:
                mapped_to, mapped_key, confidence = rule_suggestion
            else:
                mapped_to, mapped_key, confidence = ("ignored", None, 0.5)
            suggestions.append(
                {
                    "raw_value": raw,
                    "normalized_value": normalized,
                    "mapped_to": mapped_to,
                    "mapped_key": mapped_key,
                    "confidence": confidence,
                    "source": "rule",
                }
            )
        else:
            existing = (
                db.query(SemanticFieldMappingModel).filter_by(normalized_value=normalized).first()
            )
            if existing:
                # TODO this will not update DB, need to commit later
                existing.times_used += 1
                suggestions.append(
                    {
                        "raw_value": raw,
                        "normalized_value": normalized,
                        "mapped_to": existing.mapped_to,
                        "mapped_key": existing.mapped_key,
                        "confidence": existing.confidence,
                        "source": existing.source.value,
                        "times_used": existing.times_used,
                    }
                )
            else:
                if value := _cache_get(f"template_mapping:{normalized}"):
                    suggestions.append(
                        {
                            "raw_value": raw,
                            "normalized_value": normalized,
                            "mapped_to": value["mapped_to"],
                            "mapped_key": value["mapped_key"],
                            "confidence": value["confidence"],
                            "source": value.get("source", "ai"),
                        }
                    )
                else:
                    unknown.append({"raw_value": raw, "normalized_value": normalized})
    db.commit()  # commit any times_used updates

    # Use embedding-based semantic matching for unknown fields
    if unknown and embedding_model and USE_SEMANTIC_EMBEDDINGS:
        unknown_suggestions = _match_unknown_fields(unknown, db)
        for item in unknown_suggestions:
            suggestions.append(item)
            # Cache result
            _cache_set(
                f"template_mapping:{item['normalized_value']}",
                {
                    "mapped_to": item["mapped_to"],
                    "mapped_key": item.get("mapped_key"),
                    "confidence": item["confidence"],
                    "source": "semantic",
                },
                ttl=7 * 86400,
            )
        bulk_create_semantic_field_mappings(db, valid_user["id"], unknown_suggestions)
        unknown = []

    return {"suggestions": suggestions, "unknown": unknown}


ALLOWED_MAPPED_TO = [
    "budget_category",
    "budget_field",
    "extra_field",
    "header_metadata",
    "currency",
    "date_range",
    "person",
    "ignored",
    "organisation_name",
    "project_name",
    "project_reference",
    "project_duration",
    "signatury_person",
]


def _match_unknown_fields(unknown_items: List[Dict], db: Session) -> List[Dict]:
    """
    Match unknown fields using semantic embeddings against known canonical fields.

    Strategy:
    1. Try to match against existing FIELD_PATTERNS using embeddings
    2. Use similarity threshold to classify fields
    3. Return structured mappings
    """
    if not embedding_model:
        return []

    results = []

    # Build canonical field vectors
    canonical_fields = {}
    for pattern, canonical in FIELD_PATTERNS.items():
        vec = _embedding(pattern)
        canonical_fields[canonical] = vec

    # Category keywords
    category_vectors = {}
    for pattern, canonical in CATEGORY_KEYWORDS.items():
        vec = _embedding(pattern)
        category_vectors[canonical] = vec

    # Match unknown items
    for item in unknown_items:
        raw_value = item["raw_value"]
        normalized = item["normalized_value"]

        item_vec = _embedding(raw_value)

        # Try to match against budget fields
        best_field = None
        best_score_field = -1.0
        for field_name, field_vec in canonical_fields.items():
            score = _cosine(item_vec, field_vec)
            if score > best_score_field:
                best_score_field = score
                best_field = field_name

        # Try to match against budget categories
        best_category = None
        best_score_category = -1.0
        for cat_name, cat_vec in category_vectors.items():
            score = _cosine(item_vec, cat_vec)
            if score > best_score_category:
                best_score_category = score
                best_category = cat_name

        # Decide best match with confidence threshold
        SIMILARITY_THRESHOLD = 0.5

        if best_score_field > best_score_category and best_score_field > SIMILARITY_THRESHOLD:
            # Field match
            confidence = max(0.0, min(1.0, (best_score_field + 1.0) / 2.0))
            results.append(
                {
                    "raw_value": raw_value,
                    "normalized_value": normalized,
                    "mapped_to": "budget_field",
                    "mapped_key": best_field,
                    "confidence": round(confidence, 3),
                    "source": "semantic",
                }
            )
        elif best_score_category > SIMILARITY_THRESHOLD:
            # Category match
            confidence = max(0.0, min(1.0, (best_score_category + 1.0) / 2.0))
            results.append(
                {
                    "raw_value": raw_value,
                    "normalized_value": normalized,
                    "mapped_to": "budget_category",
                    "mapped_key": best_category,
                    "confidence": round(confidence, 3),
                    "source": "semantic",
                }
            )
        else:
            # Low confidence - mark as ignored
            results.append(
                {
                    "raw_value": raw_value,
                    "normalized_value": normalized,
                    "mapped_to": "ignored",
                    "mapped_key": None,
                    "confidence": 0.0,
                    "source": "semantic",
                }
            )

    return results
