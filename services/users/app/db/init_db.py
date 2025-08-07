# /services/users/app/db/init_db.py
# ⚠️ Forces model evaluation
from app.models import UserModel  # noqa: F401
from app.models import CustomerModel  # noqa: F401
from app.models import SessionModel  # noqa: F401


from app.models.base import Base
from app.db.session import engine


def init_db():
    Base.metadata.create_all(bind=engine)
