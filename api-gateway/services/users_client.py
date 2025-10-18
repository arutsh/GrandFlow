import httpx
from typing import List, Dict
from utils.gateway_wrapper import service_call_exception_handler
from shared.schemas.auth_schema import RegisterRequest

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
async def register_via_gateway(payload: RegisterRequest) -> dict:

    r = await _client.post(f"{USERS_SERVICE_URL}/register", json=payload.model_dump(mode="json"))
    r.raise_for_status()
    return r.json()


@service_call_exception_handler
async def get_users_by_ids(ids: List[str], token: str) -> Dict[str, dict]:
    if not ids:
        return {}
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # call a batch endpoint if available (recommended)
    r = await _client.post(f"{USERS_SERVICE_URL}/users/by_ids/", headers=headers, json=ids)
    r.raise_for_status()
    items = r.json()
    return {it["id"]: it for it in items}


@service_call_exception_handler
async def get_customers_by_ids(ids: List[str], token: str) -> Dict[str, dict]:
    if not ids:
        return {}
    headers = {"Authorization": f"Bearer {token}"} if token else {}

    # call a batch endpoint if available (recommended)
    r = await _client.post(f"{USERS_SERVICE_URL}/customers/by_ids/", headers=headers, json=ids)
    r.raise_for_status()
    items = r.json()
    return {it["id"]: it for it in items}
