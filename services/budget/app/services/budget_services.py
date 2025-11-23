import asyncio
from fastapi import status
from app.crud.budget_crud import (
    create_budget,
    get_budget,
    update_budget,
    list_budgets,
    delete_budget,
)
from app.core.exceptions import DomainError, PermissionDenied

from app.services.customer_client import validate_customer_type
from app.schemas.budget_schema import BudgetCreate
from uuid import UUID

from typing import List
from app.models import BudgetModel

from app.services.user_client import get_customers_by_ids, get_users_by_ids


async def create_budget_service(
    budget: BudgetCreate, valid_user: dict, db, include_user_datails: bool = False
):

    if budget.funding_customer_id:
        validate_customer_type(budget.funding_customer_id, "donor", raise_domain_error=True)

    owner_id = valid_user["customer_id"]

    if valid_user["role"] == "superuser":
        if not budget.owner_id:
            raise DomainError(
                "Superuser must specify owner_id (not associated with a customer).",
                status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        validate_customer_type(budget.owner_id, "ngo", raise_domain_error=True)

        owner_id = budget.owner_id
    new_budget = create_budget(
        session=db,
        user_id=valid_user["id"],
        name=budget.name,
        funding_customer_id=budget.funding_customer_id,
        external_funder_name=budget.external_funder_name,
        owner_id=owner_id,
    )
    if not include_user_datails:
        return new_budget
    result = await populate_budget_with_user_details([new_budget], valid_user=valid_user)

    return result[0]


async def update_budget_service(budget_id: UUID, budget: BudgetCreate, valid_user: dict, db):

    if budget.funding_customer_id:
        validate_customer_type(budget.funding_customer_id, "donor", raise_domain_error=True)

    valid_budget = await get_budget_service(budget_id=budget_id, valid_user=valid_user, db=db)

    owner_id = valid_user["customer_id"]

    if valid_user["role"] == "superuser" and budget.owner_id:
        validate_customer_type(budget.owner_id, "ngo", raise_domain_error=True)
        owner_id = budget.owner_id

    elif valid_user["role"] != "superuser":
        # checks if customer has right to update the budget
        if (budget.owner_id and valid_budget.owner_id != budget.owner_id) or (
            valid_user["customer_id"] != valid_budget.owner_id
        ):
            raise PermissionDenied()

    return update_budget(
        session=db,
        budget_id=budget_id,
        name=budget.name,
        owner_id=owner_id,
        funding_customer_id=budget.funding_customer_id,
        external_funder_name=budget.external_funder_name,
    )


async def get_budget_service(budget_id, valid_user, db, include_user_details: bool = False):

    budget = (
        get_budget(db, budget_id)
        if valid_user["role"] == "superuser"
        else get_budget(db, budget_id, valid_user["customer_id"])
    )
    if not budget:
        raise DomainError(
            "Budget Not found",
            status.HTTP_400_BAD_REQUEST,
        )
    if not include_user_details:
        return budget
    result = await populate_budget_with_user_details([budget], valid_user)
    return result[0]


async def list_budget_service(valid_user, db, include_user_details: bool = False):
    if valid_user["role"] == "superuser":
        return list_budgets(db)

    budgets = list_budgets(db, customer_id=valid_user["customer_id"])
    if not include_user_details:
        return budgets
    return await populate_budget_with_user_details(budgets=budgets, valid_user=valid_user)


async def delete_budget_service(budget_id: UUID, valid_user: dict, db):
    # fetch valid budget, if user does not have access relevant error will be raised
    valid_budget = await get_budget_service(budget_id=budget_id, valid_user=valid_user, db=db)

    if valid_budget:
        return delete_budget(session=db, budget=valid_budget)
    return False


async def populate_budget_with_user_details(budgets: List[BudgetModel], valid_user: dict):
    # Collect unique user and customer IDs
    user_ids = {b.created_by for b in budgets if b.created_by}
    user_ids |= {b.updated_by for b in budgets if b.updated_by}
    customer_ids = {b.funding_customer_id for b in budgets if b.funding_customer_id}
    customer_ids |= {b.owner_id for b in budgets if b.owner_id}
    user_ids = user_ids if user_ids else set()
    customer_ids = customer_ids if customer_ids else set()
    # Fetch users/customers concurrently
    users_task = asyncio.create_task(get_users_by_ids(list(user_ids), valid_user.get("token")))
    customers_task = asyncio.create_task(
        get_customers_by_ids(list(customer_ids), valid_user.get("token"))
    )
    users_map, customers_map = await asyncio.gather(users_task, customers_task)

    # Merge enriched data
    enriched = [
        {
            "id": b.id,
            "name": b.name,
            "status": b.status,
            "duration_months": b.duration_months,
            "local_currency": b.local_currency,
            "owner": customers_map.get(b.owner_id),
            "funder": customers_map.get(b.funding_customer_id) or {"name": b.external_funder_name},
            "trace": {
                "created": {
                    "user": users_map.get(b.created_by),
                    "event_date": b.created_at,
                },
                "updated": {
                    "user": users_map.get(b.updated_by),
                    "event_date": b.updated_at,
                },
            },
        }
        for b in budgets
    ]
    return enriched
