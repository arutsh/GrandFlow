from abc import ABC, abstractmethod
from typing import AsyncIterator


class BaseProvider(ABC):
    @abstractmethod
    async def stream(self, prompt: str) -> AsyncIterator[str]:
        raise NotImplementedError

    @abstractmethod
    async def complete(self, prompt: str) -> str:
        raise NotImplementedError


class NullProvider(BaseProvider):
    """Returns ai_available=False for every request. Used when no AI key is configured."""

    async def stream(self, prompt: str) -> AsyncIterator[str]:
        async def _gen():
            yield "event: unavailable\ndata: {}\n\n"

        return _gen()

    async def complete(self, prompt: str) -> str:
        return ""


def resolve_provider(env: str) -> BaseProvider:
    return NullProvider()
