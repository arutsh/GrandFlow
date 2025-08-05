# /services/budget/app/schemas/budget.py
from pydantic import BaseModel, ConfigDict


class BudgetLine(BaseModel):
    description: str
    amount: float


class Budget(BaseModel):
    name: str
    customer_id: str
    lines: list[BudgetLine]

    model_config = ConfigDict(from_attributes=True)
