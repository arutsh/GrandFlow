from pydantic import BaseModel
from enum import Enum


class CustomerType(str, Enum):
    donor = "donor"
    ngo = "ngo"


class Customer(BaseModel):
    id: str | None = None
    name: str
    country: str
    type: CustomerType
    currency: str

    class Config:
        orm_mode = True
