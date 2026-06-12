from datetime import datetime
from uuid import UUID, uuid4
from typing import Any, Dict
from pydantic import BaseModel, Field


class BaseEvent(BaseModel):
    """
    Base schema for all system events.
    Include standard metadata required for tracking and routing in a message broker
    (e.g., RabbitMQ).
    """

    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    event_type: str  # e.g., "user.updated", "budget.created"
    payload: Dict[str, Any]

    model_config = {"from_attributes": True}


class UserUpdatedEvent(BaseEvent):
    """
    Specific event triggered when a user's information is updated in the User Service.
    The Budget Service listens for this to update its local cache.
    """

    event_type: str = "user.updated"
    # The payload should contain relevant fields like user_id, email, or status.


class BudgetCreatedEvent(BaseEvent):
    """
    Specific event triggered when a new budget is created.
    Other services can listen to this for downstream processing (e.g., notifications).
    """

    event_type: str = "budget.created"
    # The payload should contain relevant fields like budget_id, user_id, amount, etc.
