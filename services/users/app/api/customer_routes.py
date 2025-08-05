from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from ..schemas.customer_schema import Customer
from ..models.customer import CustomerModel
from ..db.session import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/customers/", response_model=list[Customer])
def list_customers(db: Session = Depends(get_db)):
    return db.query(CustomerModel).all()


@router.post("/customers/", response_model=Customer)
def create_customer(customer: Customer, db: Session = Depends(get_db)):
    customer.id = str(uuid4())
    db_customer = CustomerModel(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: str, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
