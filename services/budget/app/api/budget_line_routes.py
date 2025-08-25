# /services/budget/app/api/budget_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import List

from app.db.session import SessionLocal
from app.models.budget import BudgetLineModel
from app.schemas.budget_schema import BudgetLine
from app.utils.security import get_current_user

router = APIRouter(prefix="/budget-lines", tags=["Budget Lines"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[BudgetLine])
def get_budget_lines(db: Session = Depends(get_db), user=Depends(get_current_user)):
    budget_lines = db.query(BudgetLineModel).all()
    return budget_lines
