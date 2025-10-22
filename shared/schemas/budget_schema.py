# /services/budget/app/schemas/budget.py

from pydantic import BaseModel, ConfigDict, model_validator
from uuid import UUID
from shared.schemas.budget_line_schema import BudgetLine
from datetime import datetime


# Budget Schemas
class BudgetBase(BaseModel):
    name: str
    owner_id: UUID | None = None
    funding_customer_id: UUID | None = None
    external_funder_name: str | None = None
    created_by: UUID | None = None
    updated_by: UUID | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    @model_validator(mode="after")
    def check_funder(self):
        if not self.funding_customer_id and not self.external_funder_name:
            raise ValueError("Funding source is required")
        return self


class BudgetCreate(BudgetBase):
    pass


class Budget(BudgetBase):
    id: UUID
    lines: list[BudgetLine] = []
    model_config = ConfigDict(from_attributes=True)
