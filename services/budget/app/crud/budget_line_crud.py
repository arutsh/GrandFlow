from sqlalchemy.orm import Session
from app.models.budget import BudgetLineModel
from uuid import UUID

from app.schemas import BudgetLineCreate


def create_budget_line(
    session: Session,
    user_id: UUID,
    budget_id: UUID,
    category_id: UUID | None,
    description: str,
    amount: float,
    extra_fields: dict | None = None,
) -> BudgetLineModel:
    """
    Create a budget line after validating NGO and Donor IDs.
    """
    # Validate external customer IDs

    budget_line = BudgetLineModel(
        budget_id=budget_id,
        category_id=category_id,
        description=description,
        amount=amount,
        extra_fields=extra_fields,
        created_by=user_id,
        updated_by=user_id,
    )
    session.add(budget_line)
    session.commit()
    session.refresh(budget_line)
    return budget_line


def get_budget_line(session: Session, budget_line_id: UUID) -> BudgetLineModel | None:
    return session.query(BudgetLineModel).filter(BudgetLineModel.id == budget_line_id).first()


def list_budget_lines(
    session: Session,
    budget_id: UUID | None = None,
    customer_id: UUID | None = None,
    limit: int = 100,
):
    query = session.query(BudgetLineModel)
    if budget_id:
        query = query.filter(BudgetLineModel.budget_id == budget_id)
    if customer_id:
        query = query.filter(BudgetLineModel.customer_id == customer_id)
    return query.limit(limit).all()


def list_budget_lines_by_category(
    session: Session, category_id: UUID | None = None, limit: int = 100
):
    query = session.query(BudgetLineModel)
    if category_id:
        query = query.filter(BudgetLineModel.category_id == category_id)
    return query.limit(limit).all()


def update_budget_line(
    session: Session, existing_line, new_budget_line: BudgetLineCreate
) -> BudgetLineModel | None:

    existing_line.description = new_budget_line.description
    existing_line.amount = new_budget_line.amount
    existing_line.extra_fields = new_budget_line.extra_fields
    session.commit()
    session.refresh(existing_line)
    return existing_line


def delete_budget_line(session: Session, budget_line_id: UUID) -> bool:
    budget_line = get_budget_line(session, budget_line_id)
    if budget_line:
        session.delete(budget_line)
        session.commit()
        return True
    return False
