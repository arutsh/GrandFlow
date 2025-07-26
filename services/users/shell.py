from app.db.session import SessionLocal
from app.models import UserModel, CustomerModel

db = SessionLocal()

print("🔁 DB session loaded as `db`")
print("📦 Models: UserModel, CustomerModel")


print(db.query(UserModel).all())
