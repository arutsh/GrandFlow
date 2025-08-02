# app/models/session.py
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from .user import Base

class SessionModel(Base):
    __tablename__ = "user_sessions"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    revoked = Column(Boolean, default=False)
    refresh_token_hash = Column(String, nullable=True)

    user = relationship("UserModel", back_populates="sessions")
# UserModel.sessions = relationship("SessionModel", back_populates="user", lazy="joined")