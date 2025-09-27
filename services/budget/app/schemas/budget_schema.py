# /services/budget/app/schemas/budget.py
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from app.schemas import BudgetLine


# Budget Schemas
class BudgetBase(BaseModel):
    name: str
    owner_id: UUID
    funding_customer_id: UUID | None = None
    external_funder_name: str | None = None


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: UUID
    lines: list[BudgetLine] = []
    model_config = ConfigDict(from_attributes=True)
