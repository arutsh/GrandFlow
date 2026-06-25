import anyio
from unittest.mock import MagicMock, patch
from app.services.provider import NullProvider, AnthropicProvider, resolve_provider


class TestNullProvider:
    def test_stream_yields_unavailable_event(self):
        async def _run():
            provider = NullProvider()
            chunks = []
            async for chunk in await provider.stream("any prompt"):
                chunks.append(chunk)
            return chunks

        chunks = anyio.from_thread.run_sync(anyio.run, _run) if False else anyio.run(_run)
        assert len(chunks) == 1
        assert "event: unavailable" in chunks[0]

    def test_complete_returns_empty_string(self):
        async def _run():
            return await NullProvider().complete("any prompt")

        result = anyio.run(_run)
        assert result == ""


class TestResolveProvider:
    def _make_user_key(self, provider_name="anthropic", model_name=None, encrypted_key="enc"):
        user_key = MagicMock()
        user_key.provider.name = provider_name
        user_key.model_name = model_name
        user_key.encrypted_key = encrypted_key
        user_key.base_url = None
        return user_key

    def test_user_key_returns_anthropic_provider(self):
        user_key = self._make_user_key()
        with patch("app.utils.encryption.decrypt", return_value="sk-ant-api03-testkey"):
            provider = resolve_provider(user_key=user_key)
        assert isinstance(provider, AnthropicProvider)
        assert provider.provider_name == "anthropic"

    def test_user_key_uses_model_name(self):
        user_key = self._make_user_key(model_name="claude-haiku-4-5-20251001")
        with patch("app.utils.encryption.decrypt", return_value="sk-ant-api03-testkey"):
            provider = resolve_provider(user_key=user_key)
        assert isinstance(provider, AnthropicProvider)
        assert provider.model_name == "claude-haiku-4-5-20251001"

    def test_no_key_returns_null(self):
        provider = resolve_provider(user_key=None)
        assert isinstance(provider, NullProvider)

    def test_no_user_key_returns_null(self):
        provider = resolve_provider()
        assert isinstance(provider, NullProvider)
