from abc import ABC, abstractmethod
from typing import AsyncIterator, cast

import anthropic as anthropic_sdk
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


class AnthropicProvider(BaseProvider):
    """Anthropic Claude via the official SDK. Used for BYOK and cloud mode."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6") -> None:
        self._model = model
        self._client = anthropic_sdk.AsyncAnthropic(api_key=api_key)

    @property
    def model_name(self) -> str:
        return self._model

    @property
    def provider_name(self) -> str:
        return "anthropic"

    async def stream(self, prompt: str, system_prompt: str = "") -> AsyncIterator[str]:
        async def _gen():
            try:
                ctx = self._client.messages.stream(
                    model=self._model,
                    max_tokens=2048,
                    system=system_prompt if system_prompt else anthropic_sdk.NOT_GIVEN,  # type: ignore[arg-type]  # noqa: E501
                    messages=[{"role": "user", "content": prompt}],
                )
                async with ctx as stream:
                    async for text in stream.text_stream:
                        yield text
            except Exception as exc:
                logger.error("anthropic_stream_error", error=str(exc))
                raise

        return _gen()

    async def complete(self, prompt: str, system_prompt: str = "") -> str:
        try:
            _system = (  # type: ignore[assignment]
                system_prompt if system_prompt else anthropic_sdk.NOT_GIVEN
            )
            response = await self._client.messages.create(
                model=self._model,
                max_tokens=2048,
                system=_system,  # type: ignore[arg-type]
                messages=[{"role": "user", "content": prompt}],
            )
            return next(
                (b.text for b in response.content if isinstance(b, anthropic_sdk.types.TextBlock)),
                "",
            )
        except Exception as exc:
            logger.error("anthropic_complete_error", error=str(exc))
            raise


def resolve_provider(
    user_key=None,  # UserProviderKey | None — avoid circular import
) -> BaseProvider:
    from app.core.config import settings
    from app.utils.encryption import decrypt

    if user_key and user_key.provider:
        provider_name = user_key.provider.name
        model = user_key.model_name
        if model is None:
            raise ValueError(f"provider key for user {user_key.user_id} has no model_name set")
        if provider_name == "anthropic" and user_key.encrypted_key:
            api_key = decrypt(user_key.encrypted_key, settings.ENCRYPTION_KEY)
            return AnthropicProvider(api_key=api_key, model=model)
        if provider_name == "ollama":
            base_url = user_key.base_url or settings.OLLAMA_URL
            if base_url:
                return OllamaProvider(base_url=base_url, model=model)
    return NullProvider()
