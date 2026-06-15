import anyio
from app.services.provider import NullProvider


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
