# /services/budget/app/schemas/budget.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from uuid import UUID


class BudgetLine(BaseModel):
    id: UUID
    budget_id: UUID
    description: str
    amount: float
    extra_fields: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


class BudgetLinesResponse(BaseModel):
    budget_lines: List[BudgetLine]


class Budget(BaseModel):
    id: UUID
    # budget_id: UUID
    name: str
    ngo_id: UUID
    donor_id: UUID
    lines: list[BudgetLine]

    model_config = ConfigDict(from_attributes=True)
