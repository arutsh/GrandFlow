# /services/budget/app/models/budget.py

import uuid
from sqlalchemy import String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.utils.db import GUID

from app.models.base import Base
from shared.db.audit_mixin import AuditMixin


class BudgetModel(Base, AuditMixin):
    __tablename__ = "budgets"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(),
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4()),  # auto-generate UUID4
    )
    ngo_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)
    donor_id: Mapped[uuid.UUID] = mapped_column(GUID(), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    lines: Mapped[list["BudgetLineModel"]] = relationship(
        "BudgetLineModel", back_populates="budget"
    )


class BudgetLineModel(Base):
    __tablename__ = "budget_lines"

    id: Mapped[uuid.UUID] = mapped_column(
        GUID(), primary_key=True, index=True, default=lambda: uuid.uuid4()
    )
    budget_id: Mapped[uuid.UUID] = mapped_column(GUID(), ForeignKey("budgets.id"), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)

    # store arbitrary metadata (JSON column, default empty dict)
    extra_fields: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)

    budget: Mapped["BudgetModel"] = relationship("BudgetModel", back_populates="lines")
