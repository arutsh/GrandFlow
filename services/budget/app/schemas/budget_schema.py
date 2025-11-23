from shared.schemas.budget_schema import BudgetBase  # noqa: F401
from shared.schemas.budget_schema import BudgetCreate  # noqa: F401
from shared.schemas.budget_schema import Budget  # noqa: F401
from shared.schemas.budget_schema import BudgetUpdate  # noqa: F401
from shared.schemas.budget_schema import BudgetWithLines  # noqa: F401

from enum import Enum


class BudgetStatus(str, Enum):
    draft = "draft"
    confirmed = "confirmed"
    archived = "archived"
