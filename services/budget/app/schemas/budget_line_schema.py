# /services/budget/app/schemas/budget.py
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID

# Budget Line schema


class BudgetLineBase(BaseModel):

    budget_id: UUID
    description: str
    amount: float
    extra_fields: Optional[Dict[str, Any]] = None


class BudgetLineCreate(BudgetLineBase):
    pass


class BudgetLine(BudgetLineBase):
    id: UUID

    model_config = {"from_attributes": True}


class BudgetLinesResponse(BaseModel):
    budget_lines: List[BudgetLine]
