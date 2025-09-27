# /services/budget/app/api/budget_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas import BudgetLine, BudgetLineCreate
from app.utils.security import get_current_user
from app.crud.budget_line_crud import (
    create_budget_line,
    get_budget_line,
    list_budget_lines,
    update_budget_line,
)
from uuid import UUID

router = APIRouter(prefix="/budget-lines", tags=["Budget Lines"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[BudgetLine])
def get_budget_lines_view(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return list_budget_lines(db)


@router.post("/", response_model=BudgetLine)
def create_budget_line_view(
    budget_line: BudgetLineCreate, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    # TODO check if user has right to create budget line against budget
    return create_budget_line(
        db,
        budget_id=budget_line.budget_id,
        description=budget_line.description,
        amount=budget_line.amount,
        extra_fields=budget_line.extra_fields,
    )


@router.get("/by-budget/{budget_id}", response_model=List[BudgetLine])
def get_budget_lines_by_budget_view(
    budget_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    return list_budget_lines(db, budget_id=budget_id)


@router.get("/{budget_line_id}", response_model=BudgetLine)
def get_budget_line_view(
    budget_line_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)
):
    budget_line = get_budget_line(db, budget_line_id)
    if not budget_line:
        return {"error": "Budget line not found"}
    return budget_line


@router.put("/{budget_line_id}", response_model=BudgetLine)
def update_budget_line_view(
    budget_line_id: UUID,
    budget_line: BudgetLineCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    updated_line = update_budget_line(db, budget_line_id, budget_line)

    if not updated_line:
        return {"error": "Budget line not found"}
    return updated_line
