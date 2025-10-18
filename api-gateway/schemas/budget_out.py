from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID


class UserOut(BaseModel):
    id: Optional[UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]


class CustomerOut(BaseModel):
    id: Optional[UUID]
    name: Optional[str]
    type: Optional[str]


class BudgetOut(BaseModel):
    id: UUID
    name: str | None = None
    owner: Optional[CustomerOut] = None
    funder: Optional[CustomerOut | dict] = None
    created_by: Optional[UserOut] = None
    updated_by: Optional[UserOut] = None
