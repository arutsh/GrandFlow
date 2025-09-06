# shared/db/audit_mixin.py
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func

from shared.db.type_decorators import GUID


class AuditMixin:
    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=lambda: uuid.uuid4())

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), nullable=False
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    created_by: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), nullable=True)

    updated_by: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), nullable=True)
