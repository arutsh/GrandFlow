# /services/budget/app/api/budget_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4, UUID  # noqa: F401
from app.core.exceptions import DomainError
from app.db.session import SessionLocal
from app.schemas.budget_schema import Budget, BudgetCreate
from app.utils.security import get_current_user

from app.services.user_client import (
    get_valid_user,
)
from app.services.budget_services import (
    create_budget_service,
    get_budget_service,
    update_budget_service,
    list_budget_service,
    delete_budget_service,
)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_validated_user(user=Depends(get_current_user)):
    """
    FastAPI dependency that validates the user and returns the user object.
    Raises DomainError if validation fails.
    """
    try:
        return get_valid_user(user["user_id"], user["token"])
    except ValueError as e:
        raise DomainError(str(e))


@router.post("/budgets/")
def create_budget_endpoint(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    valid_user=Depends(get_validated_user),
):
    return create_budget_service(budget, valid_user, db)


@router.get("/budgets/{budget_id}", response_model=Budget)
def get_budget_endpoint(
    budget_id: UUID, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):

    return get_budget_service(budget_id, valid_user, db)


@router.patch("/budgets/{budget_id}", response_model=Budget)
def update_budget_endpoint(
    budget_id: UUID,
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    valid_user=Depends(get_validated_user),
):
    updated_budget = update_budget_service(
        budget_id=budget_id, budget=budget, valid_user=valid_user, db=db
    )
    if not updated_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated_budget


@router.get("/budgets/")
def get_all_budgets_endpoint(db: Session = Depends(get_db), valid_user=Depends(get_validated_user)):

    return list_budget_service(db=db, valid_user=valid_user)


@router.delete("/budgets/{budget_id}")
def delete_budget_endpoint(
    budget_id: UUID, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):
    return {"success": delete_budget_service(budget_id=budget_id, valid_user=valid_user, db=db)}
