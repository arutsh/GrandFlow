from __future__ import annotations
import uuid
import enum
from sqlalchemy import Boolean, String, ForeignKey, Float, JSON, Integer, Enum as SQLEnum, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.utils.db import GUID

from app.models.base import Base

from shared.db.audit_mixin import AuditMixin
from typing import TYPE_CHECKING
from app.schemas.budget_schema import BudgetStatus


class UploadedTemplateStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    DETECTED = "detected"
    MAPPED = "mapped"
    CONSUMED = "consumed"


class UploadedTemplateModel(Base, AuditMixin):
    __tablename__ = "uploaded_templates"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),  # auto-generate UUID4
    )

    owner_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)
    funding_customer_id: Mapped[uuid.UUID | None] = mapped_column(GUID(), nullable=True)

    file_path: Mapped[str] = mapped_column(String, nullable=False)

    detected_structure: Mapped[dict] = mapped_column(JSONB, nullable=False)

    status: Mapped[UploadedTemplateStatus] = mapped_column(
        SQLEnum(UploadedTemplateStatus, name="uploaded_template_status"),
        nullable=False,
        default=UploadedTemplateStatus.UPLOADED,
        server_default=text("'uploaded'"),
    )
    mappings: Mapped[list["TemplateToBudgetMappingModel"]] = relationship(
        back_populates="template",
        cascade="all, delete-orphan",
    )


class TemplateToBudgetMappingModel(Base):
    __tablename__ = "template_budget_mappings"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),  # auto-generate UUID4
    )

    uploaded_template_id: Mapped[uuid.UUID] = mapped_column(
        GUID,
        ForeignKey("uploaded_templates.id"),
        nullable=False,
    )

    mapping: Mapped[dict] = mapped_column(JSONB, nullable=False)

    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    template: Mapped["UploadedTemplateModel"] = relationship(back_populates="mappings")
