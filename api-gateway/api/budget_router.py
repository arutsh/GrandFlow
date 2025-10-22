import asyncio
from fastapi import APIRouter, Depends
from typing import List
from fastapi.security import OAuth2PasswordBearer
from services.budgets_client import get_budgets
from services.users_client import (
    get_customers_by_ids,
    get_users_by_ids,
)
from schemas.budget_schema import BudgetOut, BudgetCreate
from services.budgets_client import update_budget_client, delete_budget_client, create_budget_client

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.get("/budgets/", response_model=List[BudgetOut])
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
            "trace": {
                "created": {
                    "user": users_map.get(b.get("created_by")),
                    "event_date": b.get("created_at"),
                },
                "updated": {
                    "user": users_map.get(b.get("updated_by")),
                    "event_date": b.get("updated_at"),
                },
            },
        }
        for b in budgets
    ]
    return enriched


@router.patch("/budgets/{budget_id}", response_model=BudgetOut)
async def update_budget(
    budget_id: str, budget_data: BudgetCreate, token: str = Depends(oauth2_scheme)
):
    """Update a budget and return enriched data."""

    updated_budget = await update_budget_client(budget_id, budget_data, token)

    user_ids = {updated_budget["created_by"], updated_budget["updated_by"]}
    customer_ids = {
        updated_budget.get("owner_id"),
        updated_budget.get("funding_customer_id"),
    }
    user_ids.discard(None)
    customer_ids.discard(None)
    # Fetch related user and customer info
    users_task = asyncio.create_task(get_users_by_ids(list(user_ids), token))
    customers_task = asyncio.create_task(get_customers_by_ids(list(customer_ids), token))
    users_map, customers_map = await asyncio.gather(users_task, customers_task)

    enriched_budget = {
        "id": updated_budget["id"],
        "name": updated_budget["name"],
        "owner": customers_map.get(updated_budget.get("owner_id")),
        "funder": customers_map.get(updated_budget.get("funding_customer_id"))
        or {"name": updated_budget.get("external_funder_name")},
        "trace": {
            "created": {
                "user": users_map.get(updated_budget.get("created_by")),
                "event_date": updated_budget.get("created_at"),
            },
            "updated": {
                "user": users_map.get(updated_budget.get("updated_by")),
                "event_date": updated_budget.get("updated_at"),
            },
        },
        # "created_by": users_map.get(updated_budget.get("created_by")),
        # "updated_by": users_map.get(updated_budget.get("updated_by")),
        # "created_at": updated_budget.get("created_at"),
        # "updated_at": updated_budget.get("updated_at"),
    }
    return enriched_budget


@router.delete("/budgets/{budget_id}")
async def delete_budget(budget_id: str, token: str = Depends(oauth2_scheme)):
    """Delete a budget by ID."""

    result = await delete_budget_client(budget_id, token)
    return result


@router.post("/budgets/", response_model=BudgetOut)
async def create_budget(budget_data: BudgetCreate, token: str = Depends(oauth2_scheme)):
    """Create a new budget and return enriched data."""

    created_budget = await create_budget_client(budget_data, token)

    user_ids = {created_budget["created_by"], created_budget["updated_by"]}
    customer_ids = {
        created_budget.get("owner_id"),
        created_budget.get("funding_customer_id"),
    }
    user_ids.discard(None)
    customer_ids.discard(None)
    # Fetch related user and customer info
    users_task = asyncio.create_task(get_users_by_ids(list(user_ids), token))
    customers_task = asyncio.create_task(get_customers_by_ids(list(customer_ids), token))
    users_map, customers_map = await asyncio.gather(users_task, customers_task)

    enriched_budget = {
        "id": created_budget["id"],
        "name": created_budget["name"],
        "owner": customers_map.get(created_budget.get("owner_id")),
        "funder": customers_map.get(created_budget.get("funding_customer_id"))
        or {"name": created_budget.get("external_funder_name")},
        "trace": {
            "created": {
                "user": users_map.get(created_budget.get("created_by")),
                "event_date": created_budget.get("created_at"),
            },
            "updated": {
                "user": users_map.get(created_budget.get("updated_by")),
                "event_date": created_budget.get("updated_at"),
            },
        },
    }
    return enriched_budget
