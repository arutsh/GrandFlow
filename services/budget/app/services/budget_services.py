from fastapi import status
from app.crud.budget_crud import create_budget
from app.core.exceptions import DomainError
from app.services.user_client import is_superuser, get_valid_user
from app.services.customer_client import validate_customer_type


def create_budget_service(budget, user, db):
    valid_user = get_valid_user(user["user_id"], user["token"])

    if budget.funding_customer_id:
        validate_customer_type(budget.funding_customer_id, "donor", raise_domain_error=True)

    owner_id = valid_user["customer_id"]

    if is_superuser(user["user_id"], user["token"]):
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
