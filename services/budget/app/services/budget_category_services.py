from sqlalchemy.orm import Session
from uuid import UUID

from app.models.budget import BudgetCategoryModel
from app.crud.budget_category_crud import (
    get_budget_category,
    create_budget_category,
    get_budget_category_by_name_and_template_id,
)
from app.core.exceptions import DomainError
from fastapi import status


def get_or_create_category_service(
    db: Session, valid_user: dict, category_id: UUID | None = None, category_name: str | None = None
) -> BudgetCategoryModel:
    """The service to get or create a budget category.
    the idea is if category_id is not provided, then try to fetch 'Miscellaneous' category,
    if it does not exist, create it."""

    if category_id:
        category = get_budget_category(db, category_id)
        if not category:
            raise DomainError(
                "Budget Category not found",
                status.HTTP_404_NOT_FOUND,
            )
        return category

    donor_template_id = None
    name = "Miscellaneous"
    code = "MISC"
    if category_name:
        name = category_name
        code = "_".join(category_name.split()).upper()

    category = get_budget_category_by_name_and_template_id(db, name, donor_template_id)

    if category:
        return category

    return create_budget_category(db, valid_user["id"], name, code, donor_template_id)
