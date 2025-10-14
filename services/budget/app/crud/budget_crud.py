from sqlalchemy.orm import Session
from app.models.budget import BudgetModel
from uuid import UUID


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


def get_budget(session: Session, budget_id: UUID, customer_id: UUID = None) -> BudgetModel | None:
    query = session.query(BudgetModel)
    if customer_id:
        return query.filter(
            BudgetModel.id == budget_id, BudgetModel.owner_id == customer_id
        ).first()
    return query.filter(BudgetModel.id == budget_id).first()


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


def update_budget(
    session: Session,
    budget_id: UUID,
    name: str | None = None,
    owner_id: UUID | None = None,
    funding_customer_id: UUID | None = None,
    external_funder_name: UUID | None = None,
) -> BudgetModel | None:
    budget = get_budget(session, budget_id)
    if not budget:
        return None

    budget.name = name or budget.name
    budget.owner_id = owner_id or budget.owner_id
    budget.funding_customer_id = funding_customer_id or budget.funding_customer_id
    budget.external_funder_name = external_funder_name or budget.external_funder_name
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
