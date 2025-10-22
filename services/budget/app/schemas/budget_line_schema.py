# /services/budget/app/schemas/budget.py
# from pydantic import BaseModel
# from typing import Optional, Dict, Any, List
# from uuid import UUID

# Budget Line schema
from shared.schemas.budget_line_schema import BudgetLine  # noqa: F401
from shared.schemas.budget_line_schema import BudgetLineBase  # noqa: F401
from shared.schemas.budget_line_schema import BudgetLineCreate  # noqa: F401
from shared.schemas.budget_line_schema import BudgetLinesResponse  # noqa: F401

# class BudgetLineBase(BaseModel):

#     budget_id: UUID
#     description: str
#     amount: float
#     extra_fields: Optional[Dict[str, Any]] = None


# class BudgetLineCreate(BudgetLineBase):
#     pass


# class BudgetLine(BudgetLineBase):
#     id: UUID

#     model_config = {"from_attributes": True}


# class BudgetLinesResponse(BaseModel):
#     budget_lines: List[BudgetLine]
