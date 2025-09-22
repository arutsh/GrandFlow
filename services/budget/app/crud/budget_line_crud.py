from sqlalchemy.orm import Session
from app.models.budget import BudgetLineModel
from uuid import UUID


def create_budget_line(
    session: Session,
    budget_id: UUID,
    description: str,
    amount: float,
    extra_fields: dict | None = None,
) -> BudgetLineModel:
    """
    Create a budget line after validating NGO and Donor IDs.
    """
    # Validate external customer IDs

    budget_line = BudgetLineModel(
        budget_id=budget_id, description=description, amount=amount, extra_fields=extra_fields
    )
    session.add(budget_line)
    session.commit()
    session.refresh(budget_line)
    return budget_line


def get_budget_line(session: Session, budget_line_id: str) -> BudgetLineModel | None:
    return session.query(BudgetLineModel).filter(BudgetLineModel.id == budget_line_id).first()


def list_budget_lines(session: Session, limit: int = 100):
    return session.query(BudgetLineModel).limit(limit).all()


def update_budget_line(
    session: Session, budget_line_id: str, budget_line: BudgetLineModel
) -> BudgetLineModel | None:
    existing_line = get_budget_line(session, budget_line_id)
    if not existing_line:
        return None
    existing_line.description = budget_line.description
    existing_line.amount = budget_line.amount
    existing_line.extra_fields = budget_line.extra_fields
    session.commit()
    session.refresh(existing_line)
    return existing_line


def delete_budget_line(session: Session, budget_line_id: str) -> bool:
    budget_line = get_budget_line(session, budget_line_id)
    if budget_line:
        session.delete(budget_line)
        session.commit()
        return True
    return False
