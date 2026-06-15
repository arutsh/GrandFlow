from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.services.provider import resolve_provider
from app.core.config import settings
from app.utils.security import get_validated_user

router = APIRouter(prefix="/ai", tags=["AI"])

RATE_LIMIT_STUB = str(settings.AI_RATE_LIMIT_PER_HOUR)


@router.get("/parse-budget/stream")
async def stream_parse_budget(
    text: str,
    valid_user=Depends(get_validated_user),
):
    provider = resolve_provider(settings.env)

    async def event_generator():
        async for chunk in await provider.stream(text):
            yield chunk

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "X-Accel-Buffering": "no",
            "X-RateLimit-Limit": RATE_LIMIT_STUB,
        },
    )


@router.post("/parse-budget")
async def parse_budget(
    valid_user=Depends(get_validated_user),
):
    return {"ai_available": False}
