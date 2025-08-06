# /services/users/app/db/init_db.py
from app.models import (
    UserModel,
    CustomerModel,
    SessionModel,
)  # ⚠️ Forces model evaluation
from app.models.base import Base
from app.db.session import engine


def init_db():
    Base.metadata.create_all(bind=engine)
