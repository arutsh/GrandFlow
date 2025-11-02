from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from shared.schemas.budget_schema import BudgetCreate, Budget, BudgetBase  # noqa: F401
from shared.schemas.budget_line_schema import BudgetCategory, BudgetLine  # noqa: F401
from datetime import datetime


class UserOut(BaseModel):
    id: Optional[UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]


class CustomerOut(BaseModel):
    id: Optional[UUID]
    name: Optional[str]
    type: Optional[str]


class TraceEvent(BaseModel):
    user: Optional[UserOut] = None
    event_date: Optional[str] = None


class TraceOut(BaseModel):
    created: Optional[TraceEvent]
    updated: Optional[TraceEvent]


class BudgetOut(BaseModel):
    id: UUID
    name: str | None = None
    owner: Optional[CustomerOut] = None
    funder: Optional[CustomerOut | dict] = None
    trace: Optional[TraceOut] = None
