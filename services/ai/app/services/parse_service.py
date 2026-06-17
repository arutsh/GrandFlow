import time
from typing import AsyncIterator

from jinja2 import Template
from pydantic import ValidationError

from app.schemas.ai_schema import LLMBudgetOutput, ParseBudgetResponse
from app.services.audit import write_audit_log
from app.services.prompt_loader import load_prompt
from app.services.provider import BaseProvider
from app.core.logging import get_logger

logger = get_logger(__name__)


async def build_parse_stream(
    *,
    text: str,
    provider: BaseProvider,
    customer_id: str,
    user_id: str,
) -> AsyncIterator[str]:
    """Load prompt, stream tokens from provider, emit SSE events, write audit log.

    Yields raw SSE lines. Callers wrap this in StreamingResponse.
    On prompt load failure yields a single `event: unavailable` and returns.
    """
    try:
        loaded_prompt = await load_prompt("parse_budget")
        user_message = Template(loaded_prompt.user_template).render(text=text)
        prompt_version = loaded_prompt.version
        system_prompt = loaded_prompt.system_prompt
    except Exception as exc:
        logger.error("prompt_load_failed", error=str(exc))
        yield "event: unavailable\ndata: {}\n\n"
        return

    async for event in _stream_events(
        text=text,
        user_message=user_message,
        system_prompt=system_prompt,
        prompt_version=prompt_version,
        provider=provider,
        customer_id=customer_id,
        user_id=user_id,
    ):
        yield event


async def _stream_events(
    *,
    text: str,
    user_message: str,
    system_prompt: str,
    prompt_version: str,
    provider: BaseProvider,
    customer_id: str,
    user_id: str,
) -> AsyncIterator[str]:
    start = time.monotonic()
    accumulated = ""
    success = True
    error_message = None
    output_json = None

    try:
        yield 'event: progress\ndata: {"status": "Analyzing your description..."}\n\n'

        async for token in await provider.stream(user_message, system_prompt=system_prompt):
            accumulated += token

        yield 'event: progress\ndata: {"status": "Building budget preview..."}\n\n'

        try:
            llm_output = LLMBudgetOutput.model_validate_json(accumulated)
            response = ParseBudgetResponse(
                **llm_output.model_dump(),
                prompt_version=prompt_version,
            )
            output_json = response.model_dump()
            yield f"event: done\ndata: {response.model_dump_json()}\n\n"
        except (ValidationError, ValueError):
            success = False
            error_message = "invalid_llm_output"
            yield "event: error\ndata: try rephrasing\n\n"

    except Exception as exc:
        success = False
        error_message = str(exc)
        logger.error(
            "ai_provider_error", error=error_message, customer_id=customer_id, user_id=user_id
        )
        yield "event: error\ndata: unexpected error\n\n"
    finally:
        duration_ms = int((time.monotonic() - start) * 1000)
        try:
            await write_audit_log(
                customer_id=customer_id,
                user_id=user_id,
                prompt_version=prompt_version,
                input_text=text,
                output_json=output_json,
                provider=provider.provider_name,
                model=provider.model_name,
                success=success,
                error_message=error_message,
                duration_ms=duration_ms,
            )
        except Exception as exc:
            logger.error(
                "audit_log_write_failed",
                error=str(exc),
                customer_id=customer_id,
                user_id=user_id,
            )
