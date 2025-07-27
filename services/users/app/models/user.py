# /services/users/app/models/user.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .base import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False, server_default="")
    last_name = Column(String, nullable=False, server_default="")
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)

    customer = relationship("CustomerModel", lazy="joined")
