from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from app.schemas.user_schema import User, UserCreate
from app.models.user import UserModel
from app.models.customer import CustomerModel
from app.db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Ensure customer exists
    if user.customer_id:
        customer = db.query(CustomerModel).filter(CustomerModel.id == user.customer_id).first()
        if not customer:
            raise HTTPException(status_code=400, detail="Invalid customer_id")

    db_user = UserModel(id=str(uuid4()), **user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
