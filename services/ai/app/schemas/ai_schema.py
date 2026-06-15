from pydantic import BaseModel
from shared.schemas.budget_with_lines_schema import BudgetLineInput  # noqa: F401


class ParseBudgetRequest(BaseModel):
    text: str


class ParseBudgetResponse(BaseModel):
    budget_name: str
    external_funder_name: str
    duration_months: int | None = None
    lines: list[BudgetLineInput]
    ai_available: bool = True
    prompt_version: str
