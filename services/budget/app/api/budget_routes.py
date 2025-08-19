# /services/budget/app/api/budget_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db.session import SessionLocal
from app.models.budget import BudgetModel, BudgetLineModel
from app.schemas.budget_schema import Budget
from app.utils.security import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/budgets/")
def create_budget(budget: Budget, db: Session = Depends(get_db), user=Depends(get_current_user)):
    budget_id = str(uuid4())
    db_budget = BudgetModel(id=budget_id, name=budget.name, customer_id=budget.customer_id)
    db.add(db_budget)
    db.commit()

    for line in budget.lines:
        db_line = BudgetLineModel(
            id=str(uuid4()),
            budget_id=budget_id,
            description=line.description,
            amount=line.amount,
        )
        db.add(db_line)
    db.commit()

    return {"id": budget_id, "status": "created"}


@router.get("/budgets/{budget_id}", response_model=Budget)
def get_budget(budget_id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    budget = db.query(BudgetModel).filter(BudgetModel.id == budget_id).first()
    if not budget:
        return {"error": "Budget not found"}
    return budget


@router.get("/budgets/")
def get_budgets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    budgets = db.query(BudgetModel).all()
    return budgets
