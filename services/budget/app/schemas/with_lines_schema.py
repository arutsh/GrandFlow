from pydantic import BaseModel
from typing import Any


class BudgetLineInput(BaseModel):
    category_name: str
    description: str
    amount: float
    extra_fields: dict[str, Any] | None = None


class CreateBudgetWithLinesRequest(BaseModel):
    budget_name: str
    external_funder_name: str
    duration_months: int | None = None
    lines: list[BudgetLineInput]
