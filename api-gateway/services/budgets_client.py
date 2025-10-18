# async client to call budgets service
import httpx
from typing import Any, List

BUDGETS_SERVICE_URL = None
_client: httpx.AsyncClient | None = None


async def init_urls(settings):
    global BUDGETS_SERVICE_URL, _client
    BUDGETS_SERVICE_URL = settings["BUDGETS_SERVICE_URL"]
    _client = httpx.AsyncClient(base_url=BUDGETS_SERVICE_URL)
    print(f"✅ Budgets client initialized: {BUDGETS_SERVICE_URL}")


async def close_urls():
    global _client
    if _client:
        await _client.aclose()
        print("🛑 Budgets client closed")


async def get_budgets(token: str) -> List[dict]:
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    r = await _client.get(f"{BUDGETS_SERVICE_URL}/budgets/", headers=headers)
    r.raise_for_status()
    return r.json()

