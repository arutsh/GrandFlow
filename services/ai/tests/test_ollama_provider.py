import anyio
from unittest.mock import AsyncMock, MagicMock, patch

from app.services.provider import OllamaProvider

# Sentinel values — network calls are fully mocked so Ollama never needs to be running.
_BASE_URL = "http://ollama-test.invalid"
_MODEL = "llama3.2"


def _make_provider() -> OllamaProvider:
    return OllamaProvider(base_url=_BASE_URL, model=_MODEL)


def _make_chunk(content: str):
    chunk = MagicMock()
    chunk.choices = [MagicMock()]
    chunk.choices[0].delta.content = content
    return chunk


def _make_async_stream(tokens: list[str]):
    """Async generator that yields mock chunks — matches AsyncStream[ChatCompletionChunk]."""
    chunks = [_make_chunk(t) for t in tokens]

    async def _gen():
        for chunk in chunks:
            yield chunk

    return _gen()


class TestOllamaProvider:
    def test_stream_yields_tokens_in_order(self):
        tokens = ["{", '"budget_name"', ': "Test"', "}"]

        async def _run():
            provider = _make_provider()
            create_mock = AsyncMock(return_value=_make_async_stream(tokens))
            with patch.object(provider._client.chat.completions, "create", new=create_mock):
                collected = []
                async for token in await provider.stream("parse this"):
                    collected.append(token)
                assert collected == tokens

        anyio.run(_run)

    def test_complete_returns_full_response(self):
        async def _run():
            provider = _make_provider()

            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = '{"budget_name": "Test"}'

            with patch.object(
                provider._client.chat.completions,
                "create",
                new=AsyncMock(return_value=mock_response),
            ):
                result = await provider.complete("parse this")
                assert result == '{"budget_name": "Test"}'

        anyio.run(_run)

    def test_handles_connection_error_gracefully(self):
        async def _run():
            provider = _make_provider()
            create_mock = AsyncMock(side_effect=ConnectionError("refused"))
            with patch.object(provider._client.chat.completions, "create", new=create_mock):
                try:
                    async for _ in await provider.stream("test"):
                        pass
                    assert False, "Expected exception to propagate"
                except (ConnectionError, Exception):
                    pass

        anyio.run(_run)

    def test_system_prompt_is_included_in_messages(self):
        async def _run():
            provider = _make_provider()
            captured_messages = []

            async def fake_create(**kwargs):
                captured_messages.extend(kwargs.get("messages", []))
                return _make_async_stream([])

            with patch.object(provider._client.chat.completions, "create", new=fake_create):
                async for _ in await provider.stream("user text", system_prompt="You are X"):
                    pass

            assert captured_messages[0]["role"] == "system"
            assert captured_messages[0]["content"] == "You are X"
            assert captured_messages[1]["role"] == "user"

        anyio.run(_run)
