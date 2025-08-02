from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    id: str
    user_id: str
    issued_at: datetime
    expires_at: datetime
    revoked: bool

    class Config:
        from_attributes = True
