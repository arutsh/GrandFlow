import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.services.audit import write_audit_log
from app.services.provider import resolve_provider
from app.services.rate_limiter import check_and_increment
from app.core.config import settings
from app.core.logging import get_logger
from app.utils.security import get_validated_user

router = APIRouter(prefix="/ai", tags=["AI"])
logger = get_logger(__name__)


@router.get("/parse-budget/stream")
async def stream_parse_budget(
    text: str,
    valid_user=Depends(get_validated_user),
):
    user_id = str(valid_user["user_id"])
    customer_id = str(valid_user["customer_id"]) if valid_user.get("customer_id") else user_id

    allowed, retry_after = await check_and_increment(customer_id)
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
            headers={
                "Retry-After": str(retry_after),
                "X-RateLimit-Limit": str(settings.AI_RATE_LIMIT_PER_HOUR),
            },
        )

    provider = resolve_provider(settings.env)

    async def event_generator():
        start = time.monotonic()
        success = True
        error_message = None

        try:
            async for chunk in await provider.stream(text):
                yield chunk
        except Exception as exc:
            success = False
            error_message = str(exc)
            logger.error(
                "ai_provider_error", error=error_message, customer_id=customer_id, user_id=user_id
            )
            yield f"event: error\ndata: unexpected error\n\n"  # noqa: F541
        finally:
            duration_ms = int((time.monotonic() - start) * 1000)
            try:
                await write_audit_log(
                    customer_id=customer_id,
                    user_id=user_id,
                    prompt_version="none",
                    input_text=text,
                    provider="none",
                    model="",
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

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "X-RateLimit-Limit": str(settings.AI_RATE_LIMIT_PER_HOUR),
        },
    )


@router.post("/parse-budget")
async def parse_budget(
    valid_user=Depends(get_validated_user),
):
    return {"ai_available": False}
