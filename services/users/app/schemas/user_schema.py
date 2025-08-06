from pydantic import BaseModel, EmailStr
from app.schemas.customer_schema import Customer


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    customer_id: str


class UserCreate(UserBase):
    class Config:
        extra = "ignore"  # 👈 Ignore unexpected fields like `id`


class User(UserBase):
    id: str
    customer: Customer | None = None

    model_config = {"from_attributes": True}
