from __future__ import annotations
import json
import re
import difflib
from typing import List, Dict, Optional
from app.core.config import settings
import numpy as np
from sqlalchemy.orm import Session
from app.models.mapping import SemanticFieldMappingModel

# Optional Redis cache
redis_client = None
REDIS_URL = settings.REDIS_URL
if REDIS_URL:
    try:
        import redis

        redis_client = redis.from_url(REDIS_URL)
    except Exception:
        redis_client = None

# Optional OpenAI (embeddings)
OPENAI_API_KEY = settings.OPENAI_API_KEY
RULE_BASED_MAPPING_ENABLED = settings.RULE_BASED_MAPPING_ENABLED
use_openai = False
if OPENAI_API_KEY:
    try:
        from openai import OpenAI

        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        use_openai = True
    except Exception:
        use_openai = False


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
    key = f"emb:{text.lower()}"
    cached = _cache_get(key)
    if cached:
        return cached

    if use_openai:
        # text-embedding-3-small is cost-effective for this use
        emb = (
            openai_client.embeddings.create(model="text-embedding-3-small", input=text)
            .data[0]
            .embedding
        )
    else:
        # Fallback: character frequency vector (very rough) just to keep code runnable
        vec = np.zeros(128, dtype=float)
        for ch in text.lower():
            if 0 <= ord(ch) < 128:
                vec[ord(ch)] += 1.0
        norm = np.linalg.norm(vec) or 1.0
        emb = (vec / norm).tolist()

    _cache_set(key, emb)
    return emb


def _cosine(a: List[float], b: List[float]) -> float:
    va, vb = np.array(a), np.array(b)
    denom = (np.linalg.norm(va) * np.linalg.norm(vb)) or 1.0
    return float(np.dot(va, vb) / denom)


def suggest_mapping(ngo_fields: List[str], donor_fields: List[str]) -> List[Dict]:
    """
    Returns [{ngo_field, donor_field, confidence}] using embeddings if available,
    else difflib fallback.
    """
    if not donor_fields:
        return []

    # If OpenAI is off, difflib is often better than fake embeddings
    if not use_openai:
        suggestions: List[Dict] = []
        for nf in ngo_fields:
            match = difflib.get_close_matches(nf, donor_fields, n=1, cutoff=0.0)
            best = match[0] if match else donor_fields[0]
            conf = difflib.SequenceMatcher(a=nf.lower(), b=best.lower()).ratio()
            suggestions.append({"ngo_field": nf, "donor_field": best, "confidence": round(conf, 3)})
        return suggestions

    # With embeddings
    donor_vecs = {df: _embedding(df) for df in donor_fields}
    out: List[Dict] = []
    for nf in ngo_fields:
        nf_vec = _embedding(nf)
        best_field, best_score = donor_fields[0], -1.0
        for df, dv in donor_vecs.items():
            score = _cosine(nf_vec, dv)
            if score > best_score:
                best_field, best_score = df, score
        out.append({"ngo_field": nf, "donor_field": best_field, "confidence": round(best_score, 3)})
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


def suggest_semantic_mapping(values: List[str], db: Session) -> Dict:
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
                            "source": "cache",
                        }
                    )
                else:
                    unknown.append({"raw_value": raw, "normalized_value": normalized})

    BATCH_SIZE = 25
    if unknown and use_openai:
        for i in range(0, len(unknown), BATCH_SIZE):
            batch = unknown[i : i + BATCH_SIZE]
            openai_suggestions = call_openai_bulk([item["raw_value"] for item in batch])
            for item, oa in zip(batch, openai_suggestions):
                item.update(
                    {
                        "mapped_to": oa["mapped_to"],
                        "mapped_key": oa.get("suggested_key"),
                        "confidence": oa["confidence"],
                    }
                )
                # Cache result
                _cache_set(
                    f"template_mapping:{item['normalized_value']}",
                    {
                        "mapped_to": item["mapped_to"],
                        "mapped_key": item["mapped_key"],
                        "confidence": item["confidence"],
                    },
                    ttl=7 * 86400,
                )
            suggestions.extend(unknown)
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


SYSTEM_PROMPT = """
You classify spreadsheet labels used in NGO budget templates.

Rules:
- Output MUST be valid JSON
- Return an array with the same order as input
- Use ONLY allowed values
- Do NOT add explanations
"""

USER_PROMPT_TEMPLATE = """
Classify the following labels:

{values}

Allowed mapped_to values:
{allowed}

Return JSON array:
[
  {{
    "raw_value": "...",
    "mapped_to": "...",
    "suggested_key": "... or null",
    "confidence": 0-1
  }}
]
"""


def call_openai_bulk(values: list[str]) -> list[dict]:
    prompt = USER_PROMPT_TEMPLATE.format(
        values="\n".join(f"- {v}" for v in values),
        allowed=", ".join(ALLOWED_MAPPED_TO),
    )

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )

    content = response.choices[0].message.content.strip()

    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        # fallback: mark all as ignored
        return [
            {
                "raw_value": v,
                "mapped_to": "ignored",
                "suggested_key": None,
                "confidence": 0.0,
            }
            for v in values
        ]

    results = []
    for item in parsed:
        if item["mapped_to"] not in ALLOWED_MAPPED_TO:
            item["mapped_to"] = "ignored"
            item["confidence"] = 0.0
        results.append(item)

    return results
