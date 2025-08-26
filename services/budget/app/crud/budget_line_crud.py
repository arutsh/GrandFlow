from sqlalchemy.orm import Session
from app.models.budget import BudgetLineModel
from uuid import UUID


def create_budget_line(
    session: Session,
    name: str,
    budget_id: UUID,
) -> BudgetLineModel:
    """
    Create a budget line after validating NGO and Donor IDs.
    """
    # Validate external customer IDs

    budget_line = BudgetLineModel(name=name, budget_id=budget_id)
    session.add(budget_line)
    session.commit()
    session.refresh(budget_line)
    return budget_line


def get_budget_line(session: Session, budget_line_id: str) -> BudgetLineModel | None:
    return session.query(BudgetLineModel).filter(BudgetLineModel.id == budget_line_id).first()


def list_budget_lines(session: Session, limit: int = 100):
    return session.query(BudgetLineModel).limit(limit).all()


def update_budget_line_name(
    session: Session, budget_line_id: str, new_name: str
) -> BudgetLineModel | None:
    budget_line = get_budget_line(session, budget_line_id)
    if budget_line:
        budget_line.name = new_name
        session.commit()
        session.refresh(budget_line)
    return budget_line


def delete_budget_line(session: Session, budget_line_id: str) -> bool:
    budget_line = get_budget_line(session, budget_line_id)
    if budget_line:
        session.delete(budget_line)
        session.commit()
        return True
    return False
