# /services/budget/app/api/budget_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4, UUID  # noqa: F401

from app.db.session import SessionLocal
from app.schemas.budget_schema import Budget, BudgetBase, BudgetCreate
from app.utils.security import get_current_user
from app.crud.budget_crud import create_budget, get_budget, list_budgets, update_budget

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/budgets/")
def create_budget_endpoint(
    budget: BudgetCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):

    db_budget = create_budget(session=db, budget=budget, user_id=user["user_id"])
    # Will keep if later needed
    # for line in budget.lines:
    #     db_line = BudgetLineModel(
    #         id=str(uuid4()),
    #         budget_id=db_budget.id,
    #         description=line.description,
    #         amount=line.amount,
    #     )
    #     db.add(db_line)
    # db.commit()

    return {"id": db_budget.id, "status": "created", "budget": db_budget}


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
def get_budgets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return list_budgets(db)
