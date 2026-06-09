from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.utils.db import GUID


class UserProfileModel(Base):
    __tablename__ = "user_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        index=True,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    first_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    customer_id: Mapped[uuid.UUID | None] = mapped_column(
        GUID(),
        nullable=True,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    cached_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )
