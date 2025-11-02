from fastapi import APIRouter, Depends
from typing import List
from fastapi.security import OAuth2PasswordBearer
from schemas.budget_schema import BudgetLine
from services.budget_lines_client import list_budget_lines_endpoint_by_budget_id_client

router = APIRouter(prefix="/budget-lines", tags=["Budget Lines"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.get("/by-budget/{budget_id}", response_model=List[BudgetLine])
async def list_budget_lines_endpoint_by_budget_id(
    budget_id: str, token: str = Depends(oauth2_scheme)
):
    """Fetch budget lines for the given budget_id."""

    return await list_budget_lines_endpoint_by_budget_id_client(budget_id, token)
