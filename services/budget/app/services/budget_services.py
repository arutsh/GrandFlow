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


def create_budget_service(budget: BudgetCreate, valid_user: dict, db):

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

    return create_budget(
        session=db,
        user_id=valid_user["id"],
        name=budget.name,
        funding_customer_id=budget.funding_customer_id,
        external_funder_name=budget.external_funder_name,
        owner_id=owner_id,
    )


def update_budget_service(budget_id: UUID, budget: BudgetCreate, valid_user: dict, db):

    if budget.funding_customer_id:
        validate_customer_type(budget.funding_customer_id, "donor", raise_domain_error=True)

    owner_id = valid_user["customer_id"]

    if valid_user["role"] == "superuser" and budget.owner_id:
        validate_customer_type(budget.owner_id, "ngo", raise_domain_error=True)
        owner_id = budget.owner_id

    elif valid_user["role"] != "superuser" and (
        not budget.owner_id or valid_user["customer_id"] != budget.owner_id
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


def get_budget_service(budget_id, valid_user, db):

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
    return budget


def list_budget_service(valid_user, db):
    if valid_user["role"] == "superuser":
        return list_budgets(db)

    return list_budgets(db, customer_id=valid_user["customer_id"])


def delete_budget_service(budget_id: UUID, valid_user: dict, db):
    # fetch valid budget, if user does not have access relevant error will be raised
    valid_budget = get_budget_service(budget_id=budget_id, valid_user=valid_user, db=db)

    if valid_budget:
        return delete_budget(session=db, budget=valid_budget)
    return False
