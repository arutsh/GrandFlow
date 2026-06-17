import json
import anyio
import fakeredis
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.prompt import AIPrompt
from app.services.prompt_loader import load_prompt, _cache_key, CACHE_TTL_SECONDS


def _make_mock_prompt(name="parse_budget", version="v1") -> AIPrompt:
    prompt = AIPrompt()
    prompt.name = name
    prompt.version = version
    prompt.is_active = True
    prompt.system_prompt = "You are a helpful extractor."
    prompt.user_template = "{{ text }}"
    return prompt


def _make_mock_session(prompt: AIPrompt | None):
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = prompt
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session_class = MagicMock()
    mock_session_class.return_value.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_class.return_value.__aexit__ = AsyncMock(return_value=False)
    return mock_session_class


class TestPromptLoader:
    def test_loads_active_prompt_by_name(self):
        fake_redis = fakeredis.FakeAsyncRedis(decode_responses=True)
        mock_session_class = _make_mock_session(_make_mock_prompt())

        async def _run():
            with (
                patch("app.services.prompt_loader._get_redis", return_value=fake_redis),
                patch("app.services.prompt_loader.AsyncSessionLocal", mock_session_class),
            ):
                result = await load_prompt("parse_budget")
                assert result.name == "parse_budget"
                assert result.version == "v1"
                assert "extractor" in result.system_prompt
                assert "{{ text }}" in result.user_template

        anyio.run(_run)

    def test_caches_prompt_in_redis(self):
        fake_redis = fakeredis.FakeAsyncRedis(decode_responses=True)
        mock_session_class = _make_mock_session(_make_mock_prompt())

        async def _run():
            with (
                patch("app.services.prompt_loader._get_redis", return_value=fake_redis),
                patch("app.services.prompt_loader.AsyncSessionLocal", mock_session_class),
            ):
                await load_prompt("parse_budget")
                raw = await fake_redis.get(_cache_key("parse_budget"))
                assert raw is not None
                data = json.loads(raw)
                assert data["name"] == "parse_budget"
                assert data["version"] == "v1"
                ttl = await fake_redis.ttl(_cache_key("parse_budget"))
                assert 0 < ttl <= CACHE_TTL_SECONDS

        anyio.run(_run)

    def test_cache_miss_falls_back_to_db(self):
        """Second call with warm cache skips DB; third call after invalidation hits DB again."""
        fake_redis = fakeredis.FakeAsyncRedis(decode_responses=True)
        mock_session_class = _make_mock_session(_make_mock_prompt())

        async def _run():
            with (
                patch("app.services.prompt_loader._get_redis", return_value=fake_redis),
                patch("app.services.prompt_loader.AsyncSessionLocal", mock_session_class) as db_cls,
            ):
                # Cold load — hits DB
                await load_prompt("parse_budget")
                first_call_count = db_cls.call_count

                # Warm load — served from Redis, DB not called again
                await load_prompt("parse_budget")
                assert db_cls.call_count == first_call_count

                # Invalidate cache — next load hits DB
                await fake_redis.delete(_cache_key("parse_budget"))
                await load_prompt("parse_budget")
                assert db_cls.call_count > first_call_count

        anyio.run(_run)

    def test_raises_if_no_active_prompt_found(self):
        fake_redis = fakeredis.FakeAsyncRedis(decode_responses=True)
        mock_session_class = _make_mock_session(None)

        async def _run():
            with (
                patch("app.services.prompt_loader._get_redis", return_value=fake_redis),
                patch("app.services.prompt_loader.AsyncSessionLocal", mock_session_class),
            ):
                try:
                    await load_prompt("nonexistent")
                    assert False, "Expected ValueError"
                except ValueError as exc:
                    assert "nonexistent" in str(exc)

        anyio.run(_run)
