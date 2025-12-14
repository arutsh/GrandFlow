# /services/budget/app/schemas/budget.py

from pydantic import BaseModel, ConfigDict, model_validator
from uuid import UUID
from shared.schemas.budget_line_schema import BudgetLine
from datetime import datetime

from enum import Enum


class BudgetStatus(str, Enum):
    draft = "draft"
    confirmed = "confirmed"
    archived = "archived"


# Budget Schemass
class BudgetBase(BaseModel):
    name: str | None = None
    owner_id: UUID | None = None
    funding_customer_id: UUID | None = None
    local_currency: str | None = None
    status: BudgetStatus = BudgetStatus.draft
    duration_months: int | None = None
    external_funder_name: str | None = None
    created_by: UUID | None = None
    updated_by: UUID | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None


class BudgetCreate(BudgetBase):
    name: str

    @model_validator(mode="after")
    def check_funder(self):
        if not self.funding_customer_id and not self.external_funder_name:
            raise ValueError("Funding source is required")
        return self


class BudgetUpdate(BudgetBase):
    id: UUID | None = None


class Budget(BudgetBase):
    id: UUID
    lines: list[BudgetLine] = []
    model_config = ConfigDict(from_attributes=True)


class CustomerOut(BaseModel):
    id: UUID | None = None
    name: str | None = None
    type: str | None = None


class UserOut(BaseModel):
    id: UUID | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


class TraceEvent(BaseModel):
    user: UserOut
    event_date: datetime


class TraceOut(BaseModel):
    created: TraceEvent
    updated: TraceEvent


class BudgetWithLines(BaseModel):
    id: UUID
    name: str
    owner: CustomerOut
    funder: CustomerOut
    trace: TraceOut
    lines: list[BudgetLine] = []
    model_config = ConfigDict(from_attributes=True)
