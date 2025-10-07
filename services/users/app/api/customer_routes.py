from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.customer_schema import Customer
from app.db.session import SessionLocal
from app.crud.customer_crud import create_customer, get_customers, get_customer
from uuid import UUID

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/customers/", response_model=list[Customer])
def list_customers(db: Session = Depends(get_db)):
    return get_customers(session=db)


@router.post("/customers/", response_model=Customer)
def create_customer_endpoint(customer: Customer, db: Session = Depends(get_db)):

    db_customer = create_customer(
        session=db,
        name=customer.name,
        type=customer.type,
        country=customer.country,
        currency=customer.currency,
    )
    return db_customer


@router.get("/customers/{customer_id}", response_model=Customer)
def get_customer_endpoint(customer_id: UUID, db: Session = Depends(get_db)):
    customer = get_customer(session=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer
