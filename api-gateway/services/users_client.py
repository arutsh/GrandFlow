import httpx
from typing import List, Dict
from utils.gateway_wrapper import service_call_exception_handler
from shared.schemas.auth_schema import RegisterRequest
from shared.schemas.user_schema import UserUpdate

USERS_SERVICE_URL = None
_client: httpx.AsyncClient = None


async def init_urls(settings):
    global USERS_SERVICE_URL, _client

    USERS_SERVICE_URL = settings["USERS_SERVICE_URL"]
    _client = httpx.AsyncClient(base_url=USERS_SERVICE_URL)
    print(f"✅ Users client initialized: {USERS_SERVICE_URL}")


async def close_urls():
    """Gracefully close HTTP client session."""
    global _client
    if _client:
        await _client.aclose()
        print("🛑 Users client closed")


@service_call_exception_handler
async def login_via_gateway(payload: dict) -> dict:

    r = await _client.post(f"{USERS_SERVICE_URL}/auth/login", json=payload)
    r.raise_for_status()
    return r.json()


@service_call_exception_handler
async def refresh_token_via_gateway(refresh_token: str) -> dict:

    r = await _client.post(f"{USERS_SERVICE_URL}/auth/refresh?refresh_token={refresh_token}")
    r.raise_for_status()
    return r.json()


@service_call_exception_handler
async def register_via_gateway(payload: RegisterRequest) -> dict:

    r = await _client.post(f"{USERS_SERVICE_URL}/register", json=payload.model_dump(mode="json"))
    r.raise_for_status()
    return r.json()


@service_call_exception_handler
async def get_user_by_id(id: str, token: str) -> Dict[str, dict]:
    if not id:
        return {}
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # call a batch endpoint if available (recommended)
    r = await _client.get(f"{USERS_SERVICE_URL}/users/{id}", headers=headers)
    r.raise_for_status()
    items = r.json()
    return items


@service_call_exception_handler
async def update_user_via_gateway(user_id: str, payload: UserUpdate, token: str) -> Dict[str, dict]:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = await _client.patch(
        f"{USERS_SERVICE_URL}/users/{user_id}/", headers=headers, json=payload.model_dump()
    )
    r.raise_for_status()
    return r.json()
