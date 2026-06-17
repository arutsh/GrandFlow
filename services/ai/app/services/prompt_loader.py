import json
from dataclasses import dataclass

import redis.asyncio as aioredis
from sqlalchemy import select

from app.core.config import settings
from app.core.logging import get_logger
from app.db.session import AsyncSessionLocal
from app.models.prompt import AIPrompt

logger = get_logger(__name__)

CACHE_TTL_SECONDS = 300  # 5 minutes


@dataclass
class LoadedPrompt:
    name: str
    version: str
    system_prompt: str
    user_template: str


_redis_client: aioredis.Redis | None = None


def _get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client


def _cache_key(name: str) -> str:
    return f"ai_prompt:{name}:active"


async def load_prompt(name: str) -> LoadedPrompt:
    """Load the active prompt by name. Redis-cached for 5 minutes."""
    redis = _get_redis()
    cached = None
    try:
        cached = await redis.get(_cache_key(name))
    except Exception:
        logger.warning("prompt_cache_read_failed", prompt_name=name)

    if cached:
        data = json.loads(cached)
        return LoadedPrompt(**data)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(AIPrompt).where(AIPrompt.name == name, AIPrompt.is_active.is_(True))
        )
        prompt = result.scalar_one_or_none()

    if prompt is None:
        raise ValueError(f"No active prompt found for name '{name}'")

    loaded = LoadedPrompt(
        name=prompt.name,
        version=prompt.version,
        system_prompt=prompt.system_prompt,
        user_template=prompt.user_template,
    )

    try:
        await redis.set(
            _cache_key(name),
            json.dumps(
                {
                    "name": loaded.name,
                    "version": loaded.version,
                    "system_prompt": loaded.system_prompt,
                    "user_template": loaded.user_template,
                }
            ),
            ex=CACHE_TTL_SECONDS,
        )
    except Exception:
        logger.warning("prompt_cache_write_failed", prompt_name=name)

    return loaded


async def invalidate_prompt_cache(name: str) -> None:
    """Remove cached prompt so the next load hits the DB."""
    try:
        redis = _get_redis()
        await redis.delete(_cache_key(name))
    except Exception:
        logger.warning("prompt_cache_invalidate_failed", prompt_name=name)
