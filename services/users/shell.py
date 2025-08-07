from app.db.session import SessionLocal  # noqa: F401
from app.models import UserModel, CustomerModel  # noqa: F401

db = SessionLocal()

print("🔁 DB session loaded as `db`")
print("📦 Models: UserModel, CustomerModel")


print(db.query(UserModel).all())
