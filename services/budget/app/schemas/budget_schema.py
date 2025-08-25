# /services/budget/app/schemas/budget.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List


class BudgetLine(BaseModel):
    id: str
    budget_id: str
    description: str
    amount: float
    extra_fields: Optional[Dict[str, Any]] = None

    model_config = {"from_attributes": True}


class BudgetLinesResponse(BaseModel):
    budget_lines: List[BudgetLine]


class Budget(BaseModel):
    id: str
    # budget_id: str
    name: str
    ngo_id: str
    donor_id: str
    lines: list[BudgetLine]

    model_config = ConfigDict(from_attributes=True)
