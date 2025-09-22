# /services/budget/app/schemas/budget.py
from pydantic import BaseModel, ConfigDict
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


# Budget Schemas
class BudgetBase(BaseModel):
    name: str
    ngo_id: UUID
    donor_id: UUID
    lines: list[BudgetLine]


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)
