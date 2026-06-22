import uuid
from sqlalchemy import Boolean, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base
from app.utils.db import GUID


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=False)
    is_ngo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_donor: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    currency = mapped_column(String, nullable=False)
    users = relationship("UserModel", back_populates="customer")
