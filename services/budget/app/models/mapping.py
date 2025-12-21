from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, ForeignKey
from app.models.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.budget import BudgetCategoryModel


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
