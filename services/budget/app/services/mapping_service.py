from __future__ import annotations
import json
import difflib
from typing import List, Dict, Optional
from app.core.config import settings
import numpy as np

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

use_openai = False
if OPENAI_API_KEY:
    try:
        from openai import OpenAI

        openai_client = OpenAI(api_key=OPENAI_API_KEY)
        use_openai = True
    except Exception:
        use_openai = False


def _cache_get(key: str) -> Optional[List[float]]:
    if not redis_client:
        return None
    raw = redis_client.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def _cache_set(key: str, value: List[float], ttl: int = 86400) -> None:
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
