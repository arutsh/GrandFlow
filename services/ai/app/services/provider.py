from abc import ABC, abstractmethod
from typing import AsyncIterator, cast

from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessageParam

from app.core.logging import get_logger

logger = get_logger(__name__)


class BaseProvider(ABC):
    @abstractmethod
    async def stream(self, prompt: str, system_prompt: str = "") -> AsyncIterator[str]:
        raise NotImplementedError

    @abstractmethod
    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        raise NotImplementedError

    @property
    def provider_name(self) -> str:
        return self.__class__.__name__.lower().replace("provider", "")

    @property
    def model_name(self) -> str:
        return ""


class NullProvider(BaseProvider):
    """Returns ai_available=False for every request. Used when no AI key is configured."""

    async def stream(self, prompt: str, system_prompt: str = "") -> AsyncIterator[str]:
        async def _gen():
            yield "event: unavailable\ndata: {}\n\n"

        return _gen()

    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        return ""

    @property
    def provider_name(self) -> str:
        return "none"


class OllamaProvider(BaseProvider):
    """Ollama via OpenAI-compatible API. Used in development mode."""

    def __init__(self, base_url: str, model: str) -> None:
        self._model = model
        self._client = AsyncOpenAI(
            base_url=f"{base_url.rstrip('/')}/v1",
            api_key="ollama",
        )

    @property
    def model_name(self) -> str:
        return self._model

    async def stream(self, prompt: str, system_prompt: str = "") -> AsyncIterator[str]:
        messages: list[ChatCompletionMessageParam] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        async def _gen():
            try:
                response = cast(
                    AsyncStream[ChatCompletionChunk],
                    await self._client.chat.completions.create(
                        model=self._model,
                        messages=messages,
                        stream=True,
                        temperature=0,
                    ),
                )
                async for chunk in response:
                    delta = chunk.choices[0].delta.content
                    if delta:
                        yield delta
            except Exception as exc:
                logger.error("ollama_stream_error", error=str(exc))
                raise

        return _gen()

    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        messages: list[ChatCompletionMessageParam] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=0,
            )
            return response.choices[0].message.content or ""
        except Exception as exc:
            logger.error("ollama_complete_error", error=str(exc))
            raise


def resolve_provider(env: str) -> BaseProvider:
    from app.core.config import settings

    if env == "development" and settings.OLLAMA_URL:
        return OllamaProvider(base_url=settings.OLLAMA_URL, model=settings.OLLAMA_MODEL)
    return NullProvider()
