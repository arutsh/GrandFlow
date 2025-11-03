# /services/budget/app/api/budget_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4, UUID  # noqa: F401
from app.core.exceptions import DomainError
from app.db.session import SessionLocal
from app.schemas.budget_schema import BudgetCreate, BudgetUpdate, BudgetWithLines
from app.utils.security import get_current_user
from app.services.budget_line_services import get_budget_lines_service
from app.services.user_client import get_valid_user
from app.services.budget_services import (
    create_budget_service,
    get_budget_service,
    update_budget_service,
    list_budget_service,
    delete_budget_service,
)


router = APIRouter(prefix="/budgets", tags=["Public Budgets"])
private_router = APIRouter(prefix="/budgets", tags=["Private Budgets"])


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


@router.post("/")
async def create_budget_endpoint(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    valid_user=Depends(get_validated_user),
):
    return await create_budget_service(budget, valid_user, db, include_user_datails=True)


@router.get("/{budget_id}", response_model=BudgetWithLines)
async def get_budget_endpoint(
    budget_id: UUID,
    db: Session = Depends(get_db),
    valid_user=Depends(get_validated_user),
):
    budget = await get_budget_service(budget_id, valid_user, db, include_user_details=True)
    if budget:
        budget_lines = get_budget_lines_service(db=db, valid_user=valid_user, budget_id=budget_id)
        budget["lines"] = budget_lines
    return budget


@router.patch("/{budget_id}", response_model=BudgetUpdate)
async def update_budget_endpoint(
    budget_id: UUID,
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    valid_user=Depends(get_validated_user),
):
    updated_budget = await update_budget_service(
        budget_id=budget_id, budget=budget, valid_user=valid_user, db=db
    )
    if not updated_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return updated_budget


@router.get("/")
async def get_all_budgets_endpoint(
    db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):

    return await list_budget_service(db=db, valid_user=valid_user, include_user_details=True)


@router.delete("/{budget_id}")
async def delete_budget_endpoint(
    budget_id: UUID, db: Session = Depends(get_db), valid_user=Depends(get_validated_user)
):
    return {
        "success": await delete_budget_service(budget_id=budget_id, valid_user=valid_user, db=db)
    }
