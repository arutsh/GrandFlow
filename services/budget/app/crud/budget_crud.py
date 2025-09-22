from sqlalchemy.orm import Session
from app.models.budget import BudgetModel
from app.services.customer_client import validate_customer_type
from uuid import UUID


def create_budget(
    session: Session, name: str, ngo_id: UUID, donor_id: UUID, user_id: UUID
) -> BudgetModel:
    """
    Create a budget after validating NGO and Donor IDs.
    """
    # Validate external customer IDs
    validate_customer_type(ngo_id, "ngo")
    validate_customer_type(donor_id, "donor")
    budget = BudgetModel(
        name=name, ngo_id=ngo_id, donor_id=donor_id, created_by=user_id, updated_by=user_id
    )
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget


def get_budget(session: Session, budget_id: str) -> BudgetModel | None:
    return session.query(BudgetModel).filter(BudgetModel.id == budget_id).first()


def list_budgets(session: Session, limit: int = 100):
    return session.query(BudgetModel).limit(limit).all()


def update_budget_name(session: Session, budget_id: str, new_name: str) -> BudgetModel | None:
    budget = get_budget(session, budget_id)
    if not budget:
        return None
    budget.name = new_name
    session.commit()
    session.refresh(budget)
    return budget


def delete_budget(session: Session, budget_id: str) -> bool:
    budget = get_budget(session, budget_id)
    if budget:
        session.delete(budget)
        session.commit()
        return True
    return False
