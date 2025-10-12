from sqlalchemy.orm import Session
from app.models.budget import BudgetModel
from app.services.customer_client import validate_customer_type
from uuid import UUID

from app.schemas.budget_schema import BudgetBase


def create_budget(
    session: Session,
    user_id: UUID,
    name: str,
    funding_customer_id: UUID | None = None,
    external_funder_name: str | None = None,
    owner_id: UUID | None = None,
) -> BudgetModel:
    """
    Create a budget after validating owner and funding customer IDs.
    """

    budget = BudgetModel(
        name=name,
        owner_id=owner_id,
        funding_customer_id=funding_customer_id,
        external_funder_name=external_funder_name,
        created_by=user_id,
        updated_by=user_id,
    )
    session.add(budget)
    session.commit()
    session.refresh(budget)
    return budget


def get_budget(session: Session, budget_id: UUID) -> BudgetModel | None:
    return session.query(BudgetModel).filter(BudgetModel.id == budget_id).first()


def list_budgets(session: Session, customer_id: UUID | None = None, limit: int = 100):
    query = session.query(BudgetModel)
    if customer_id:
        query = query.filter(BudgetModel.owner_id == customer_id)
    return query.limit(limit).all()


def update_budget_name(session: Session, budget_id: UUID, new_name: str) -> BudgetModel | None:
    budget = get_budget(session, budget_id)
    if not budget:
        return None
    budget.name = new_name
    session.commit()
    session.refresh(budget)
    return budget


def update_budget(session: Session, budget_id: UUID, new_budget: BudgetBase) -> BudgetModel | None:
    budget = get_budget(session, budget_id)
    if not budget:
        return None
    # Validate external customer IDs
    validate_customer_type(new_budget.owner_id, "ngo")
    if new_budget.funding_customer_id:
        validate_customer_type(new_budget.funding_customer_id, "donor")
    budget.name = new_budget.name
    budget.owner_id = new_budget.owner_id
    budget.funding_customer_id = new_budget.funding_customer_id
    session.commit()
    session.refresh(budget)
    return budget


def delete_budget(session: Session, budget_id: UUID) -> bool:
    budget = get_budget(session, budget_id)
    if budget:
        session.delete(budget)
        session.commit()
        return True
    return False
