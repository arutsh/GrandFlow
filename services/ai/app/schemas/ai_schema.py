from pydantic import BaseModel
from shared.schemas.budget_with_lines_schema import BudgetLineInput  # noqa: F401


class ParseBudgetRequest(BaseModel):
    text: str


class LLMBudgetOutput(BaseModel):
    """Validates the raw JSON the LLM streams back. No service-layer fields."""

    budget_name: str
    external_funder_name: str | None = None
    duration_months: int | None = None
    lines: list[BudgetLineInput]


class ParseBudgetResponse(BaseModel):
    """API response to the frontend — adds service-layer fields."""

    budget_name: str
    external_funder_name: str | None = None
    duration_months: int | None = None
    lines: list[BudgetLineInput]
    ai_available: bool = True
    prompt_version: str
