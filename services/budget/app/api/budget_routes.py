# /services/budget/app/api/budget_routes.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import uuid4, UUID  # noqa: F401

from app.db.session import SessionLocal
from app.schemas.budget_schema import Budget, BudgetBase, BudgetCreate
from app.utils.security import get_current_user
from app.crud.budget_crud import get_budget, list_budgets, update_budget
from app.services.user_client import get_user_customer_id, is_superuser
from app.services.budget_services import create_budget_service


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/budgets/")
def create_budget_endpoint(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return create_budget_service(budget, user, db)


@router.get("/budgets/{budget_id}", response_model=Budget)
def get_budget_endpoint(
    budget_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    budget = get_budget(db, budget_id)
    if not budget:
        return {"error": "Budget not found"}
    return budget


@router.put("/budgets/{budget_id}", response_model=Budget)
def update_budget_endpoint(
    budget_id: UUID,
    budget: BudgetBase,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    updated_budget = update_budget(db, budget_id, budget)
    if not updated_budget:
        return {"error": "Budget not found"}
    return updated_budget


@router.get("/budgets/")
def get_all_budgets_endpoint(
    request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)
):

    if is_superuser(user["user_id"], token=user["token"]):
        return list_budgets(db)
    customer_id = get_user_customer_id(user["user_id"], token=user["token"])
    if customer_id:
        return list_budgets(db, customer_id=customer_id)
    raise HTTPException(
        status_code=400, detail="User has no associated customer_id"
    )  # happens only if user has on going boarding
