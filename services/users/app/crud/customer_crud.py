from uuid import UUID
from sqlalchemy.orm import Session

from app.models.customer import CustomerModel, CustomerType


def get_customer(session: Session, customer_id: UUID):
    return session.query(CustomerModel).filter(CustomerModel.id == customer_id).first()


def get_customers(session: Session, limit: int = 100):
    return session.query(CustomerModel).limit(limit).all()


def create_customer(
    session: Session, name: str, type: str = "ngo", country: str = "GB", currency: str = "GBP"
) -> CustomerModel:
    if type not in ["donor", "ngo"]:
        raise ValueError("Invalid customer type. Must be 'donor' or 'ngo'.")

    type = CustomerType.ngo if type != "donor" else CustomerType.donor

    customer = CustomerModel(name=name, type=type, country=country, currency=currency)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer
