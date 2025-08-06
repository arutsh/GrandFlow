# app/models/session.py
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, validates
from datetime import datetime, timedelta, timezone
from app.models.user import Base
from app.utils.security import ACCESS_TOKEN_EXPIRE_MINUTES


class SessionModel(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    issued_at = Column(DateTime, default=func.now())
    expires_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    revoked = Column(Boolean, default=False)
    refresh_token_hash = Column(String, nullable=True)

    user = relationship("UserModel", back_populates="sessions")

    @validates("issued_at", "expires_at")
    def _strip_tzinfo(self, key, value):
        if value.tzinfo is not None:
            value = value.replace(tzinfo=None)
        return value


# UserModel.sessions = relationship("SessionModel", back_populates="user", lazy="joined")
