# /services/users/app/db/init_db.py
from ..models import UserModel, CustomerModel, SessionModel  # ⚠️ Forces model evaluation
from ..models.base import Base
from .session import engine


def init_db():
    Base.metadata.create_all(bind=engine)
