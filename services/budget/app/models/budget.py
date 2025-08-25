# /services/budget/app/models/budget.py

from sqlalchemy import String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.models.base import Base


class BudgetModel(Base):
    __tablename__ = "budgets"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    ngo_id: Mapped[str] = mapped_column(String, nullable=False)
    donor_id: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    lines: Mapped[list["BudgetLineModel"]] = relationship(
        "BudgetLineModel", back_populates="budget"
    )


class BudgetLineModel(Base):
    __tablename__ = "budget_lines"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    budget_id: Mapped[str] = mapped_column(String, ForeignKey("budgets.id"), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    amount: Mapped[float | None] = mapped_column(Float, nullable=True)

    # store arbitrary metadata (JSON column, default empty dict)
    extra_fields: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)

    budget: Mapped["BudgetModel"] = relationship("BudgetModel", back_populates="lines")
