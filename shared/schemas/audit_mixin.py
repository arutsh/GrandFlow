from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class AuditMixinBase(BaseModel):

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[UUID] = None
    updated_by: Optional[UUID] = None
