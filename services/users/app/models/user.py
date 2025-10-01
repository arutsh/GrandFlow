# /services/users/app/models/user.py
from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.models.base import Base
import enum


class UserStatus(str, enum.Enum):
    active = "active"
    pending = "pending"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    first_name = Column(String, nullable=False, server_default="")
    last_name = Column(String, nullable=False, server_default="")
    email = Column(String, unique=True, index=True, nullable=False)
    role = Column(String, nullable=False)
    hashed_password = Column(String, nullable=True)  # TODO convert to nullbale=False
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    status: Mapped[UserStatus] = mapped_column(
        Enum(UserStatus), nullable=False, default=UserStatus.pending
    )
    customer = relationship("CustomerModel", lazy="joined")
    sessions = relationship("SessionModel", back_populates="user", cascade="all, delete-orphan")
