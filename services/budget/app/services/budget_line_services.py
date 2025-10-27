from fastapi import status
from app.crud.budget_crud import (
    create_budget,
    get_budget,
    update_budget,
    list_budgets,
    delete_budget,
)
from app.crud.budget_line_crud import (
    create_budget_line,
    get_budget_line,
    list_budget_lines,
    list_budget_lines_by_category,
    update_budget_line,
)


from app.core.exceptions import DomainError, PermissionDenied
from app.services.budget_category_services import get_or_create_category_service

from app.services.customer_client import validate_customer_type
from app.schemas.budget_schema import BudgetCreate
from uuid import UUID
from app.schemas import BudgetLineCreate


def create_budget_line_service(
    db,
    valid_user: dict,
    budget_line: BudgetLineCreate,
):

    budget = (
        get_budget(db, budget_line.budget_id)
        if valid_user["role"] == "superuser"
        else get_budget(db, budget_line.budget_id, valid_user["customer_id"])
    )
    if not budget:
        raise DomainError(
            "Budget Not found",
            status.HTTP_400_BAD_REQUEST,
        )
    category = get_or_create_category_service(
        db,
        valid_user,
        category_id=budget_line.category_id,
    )

    return create_budget_line(
        db,
        user_id=valid_user["id"],
        budget_id=budget_line.budget_id,
        category_id=category.id,
        description=budget_line.description,
        amount=budget_line.amount,
        extra_fields=budget_line.extra_fields,
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


def get_budget_lines_service(
    db,
    valid_user,
    budget_id=None,
):
    if budget_id:
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

        return list_budget_lines(db, budget_id=budget_id)
    else:
        if valid_user["role"] == "superuser":
            return list_budget_lines(db)
        return list_budget_lines(db, customer_id=valid_user["customer_id"])


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
