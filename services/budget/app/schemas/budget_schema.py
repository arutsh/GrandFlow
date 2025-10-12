# /services/budget/app/schemas/budget.py
from pydantic import BaseModel, ConfigDict, model_validator
from uuid import UUID
from app.schemas import BudgetLine


# Budget Schemas
class BudgetBase(BaseModel):
    name: str
    owner_id: UUID | None = None
    funding_customer_id: UUID | None = None
    external_funder_name: str | None = None


class BudgetCreate(BudgetBase):

    @model_validator(mode="after")
    def check_funder(self):
        if not self.funding_customer_id and not self.external_funder_name:
            raise ValueError("Funding source is required")
        return self


class Budget(BudgetBase):
    id: UUID
    lines: list[BudgetLine] = []
    model_config = ConfigDict(from_attributes=True)
