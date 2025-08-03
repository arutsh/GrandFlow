from pydantic import BaseModel, field_serializer
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class Session(BaseModel):
    id: str
    user_id: str
    issued_at: datetime
    expires_at: datetime
    revoked: bool

    @field_serializer("expires_at", "created_at")
    def serialize_utc(cls, value: datetime) -> datetime:
        # Assume naive datetime from DB is in UTC
        return value.replace(tzinfo=ZoneInfo("UTC"))

    class Config:
        from_attributes = True
