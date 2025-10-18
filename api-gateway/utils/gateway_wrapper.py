import functools
import httpx
from fastapi import HTTPException, status
from typing import Callable, Awaitable, Any, TypeVar

T = TypeVar("T")


def service_call_exception_handler(
    func: Callable[..., Awaitable[T]],
) -> Callable[..., Awaitable[T]]:
    """
    Decorator that wraps async service calls (to other microservices) and
    converts httpx errors into FastAPI HTTPExceptions transparently.
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        try:
            return await func(*args, **kwargs)

        except httpx.HTTPStatusError as exc:
            # Try to extract upstream error detail
            try:
                detail = exc.response.json()
            except Exception:
                detail = exc.response.text or "Upstream service error"

            headers_to_forward = {}
            if "www-authenticate" in exc.response.headers:
                headers_to_forward["WWW-Authenticate"] = exc.response.headers["www-authenticate"]

            raise HTTPException(
                status_code=exc.response.status_code,
                detail=detail,
                headers=headers_to_forward or None,
            )

        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Could not connect to upstream service: {exc}",
            )

    return wrapper
