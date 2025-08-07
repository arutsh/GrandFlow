from sqlalchemy import Column, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from app.models.base import Base


class CustomerType(str, enum.Enum):
    donor = "donor"
    ngo = "ngo"


class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    type: Mapped[CustomerType] = mapped_column(Enum(CustomerType), nullable=False)
    currency = Column(String, nullable=False)
    users = relationship("UserModel", back_populates="customer")
