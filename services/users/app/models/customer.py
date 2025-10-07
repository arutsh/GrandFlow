import uuid
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from app.models.base import Base
from app.utils.db import GUID


class CustomerType(str, enum.Enum):
    donor = "donor"
    ngo = "ngo"


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),  # auto-generate UUID4
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[CustomerType] = mapped_column(
        Enum(CustomerType),
        nullable=False,
        default=CustomerType.ngo,
    )
    currency = Column(String, nullable=False)
    users = relationship("UserModel", back_populates="customer")
