# /services/budget/app/models/budget.py

from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.models.base import Base


class BudgetModel(Base):
    __tablename__ = "budgets"

    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, nullable=False)
    name = Column(String, nullable=False)

    lines = relationship("BudgetLineModel", back_populates="budget")


class BudgetLineModel(Base):
    __tablename__ = "budget_lines"

    id = Column(String, primary_key=True, index=True)
    budget_id = Column(String, ForeignKey("budgets.id"), nullable=False)
    description = Column(String)
    amount = Column(Float)

    budget = relationship("BudgetModel", back_populates="lines")
