import redis
import json
from app.core.config import settings
from typing import Any, Optional


redis_client = None
REDIS_URL = settings.REDIS_URL
if REDIS_URL:
    try:
        redis_client = redis.from_url(REDIS_URL)
    except Exception:
        redis_client = None


def _cache_get(key: str) -> Optional[Any]:
    if not redis_client:
        return None
    raw = redis_client.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def _cache_set(key: str, value: Any, ttl: int = 86400) -> None:
    if not redis_client:
        return
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception:
        pass


def _delete_key(key: str) -> None:
    if not redis_client:
        return
    try:
        redis_client.delete(key)
    except Exception:
        pass
