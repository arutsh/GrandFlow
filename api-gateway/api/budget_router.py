import asyncio
from fastapi import APIRouter, Depends
from typing import List
from fastapi.security import OAuth2PasswordBearer
from services.budgets_client import get_budgets
from services.users_client import (
    get_customers_by_ids,
    get_users_by_ids,
)
from schemas.budget_out import BudgetOut

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.get("/budgets", response_model=List[BudgetOut])
async def list_budgets(token: str = Depends(oauth2_scheme)):
    """Fetch budgets and enrich them with user & customer info."""

    budgets = await get_budgets(token)

    # Collect unique user and customer IDs
    user_ids = {b.get("created_by") for b in budgets if b.get("created_by")}
    user_ids |= {b.get("updated_by") for b in budgets if b.get("updated_by")}
    customer_ids = {b.get("funding_customer_id") for b in budgets if b.get("funding_customer_id")}
    customer_ids |= {b.get("owner_id") for b in budgets if b.get("owner_id")}
    user_ids = user_ids if user_ids else set()
    customer_ids = customer_ids if customer_ids else set()
    # Fetch users/customers concurrently
    users_task = asyncio.create_task(get_users_by_ids(list(user_ids), token))
    customers_task = asyncio.create_task(get_customers_by_ids(list(customer_ids), token))
    users_map, customers_map = await asyncio.gather(users_task, customers_task)

    # Merge enriched data
    enriched = [
        {
            "id": b["id"],
            "name": b["name"],
            "owner": customers_map.get(b.get("owner_id")),
            "funder": customers_map.get(b.get("funding_customer_id"))
            or {"name": b.get("external_funder_name")},
            "created_by": users_map.get(b.get("created_by")),
            "updated_by": users_map.get(b.get("updated_by")),
            "created_at": b.get("created_at"),
            "updated_at": b.get("updated_at"),
        }
        for b in budgets
    ]
    return enriched
