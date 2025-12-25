from __future__ import annotations
import uuid
from enum import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, Boolean, Enum as SQLEnum, ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base
from typing import TYPE_CHECKING
from shared.db.audit_mixin import AuditMixin
from app.utils.db import GUID

if TYPE_CHECKING:
    from app.models.budget import BudgetCategoryModel


class MappingSource(str, Enum):
    AI = "ai"
    HUMAN = "human"
    IMPORTED = "imported"


class SemanticFieldMappingModel(Base, AuditMixin):
    __tablename__ = "semantic_field_mappings"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    # what appeared in Excel
    raw_value: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
        comment="Original cell text e.g. 'Office costs'",
    )

    normalized_value: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
        comment="Normalized form for lookup (lowercase, trimmed)",
    )

    # what it maps to in your system
    mapped_to: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="budget_category | budget_field | extra_field",
    )

    mapped_key: Mapped[str] = mapped_column(
        String,
        nullable=False,
        comment="e.g. 'office_costs'",
    )

    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
    )

    source: Mapped[MappingSource] = mapped_column(
        SQLEnum(MappingSource),
        nullable=False,
    )

    times_used: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    approved: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        comment="Human-confirmed mapping",
    )

    meta_data: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True,
        comment="AI reasoning, alternatives, examples",
    )


class DonorTemplateModel(Base):
    __tablename__ = "donor_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    fields: Mapped[list["DonorFieldModel"]] = relationship(
        back_populates="template", cascade="all, delete-orphan"
    )

    categories: Mapped[list["BudgetCategoryModel"]] = relationship(
        back_populates="donor_template", cascade="all, delete-orphan"
    )


class DonorFieldModel(Base):
    __tablename__ = "donor_fields"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    donor_template_id: Mapped[int] = mapped_column(
        ForeignKey("donor_templates.id", ondelete="CASCADE"), index=True
    )
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)

    template: Mapped["DonorTemplateModel"] = relationship(back_populates="fields")
    mappings: Mapped[list["NgoMappingModel"]] = relationship(
        back_populates="donor_field", cascade="all, delete-orphan"
    )


class NgoMappingModel(Base):
    __tablename__ = "ngo_mappings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # Customer (NGO) id string/uuid from users-service JWT
    owner_id: Mapped[str] = mapped_column(String(64), index=True)
    owner_field: Mapped[str] = mapped_column(String(255), nullable=False)

    donor_field_id: Mapped[int] = mapped_column(
        ForeignKey("donor_fields.id", ondelete="CASCADE"), index=True
    )
    confidence: Mapped[float] = mapped_column(Float, nullable=False)

    donor_field: Mapped["DonorFieldModel"] = relationship(back_populates="mappings")
