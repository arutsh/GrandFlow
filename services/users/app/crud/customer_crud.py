from uuid import UUID
from sqlalchemy.orm import Session

from app.models.customer import CustomerModel


def get_customer(session: Session, customer_id: UUID):
    return session.query(CustomerModel).filter(CustomerModel.id == customer_id).first()


def get_customers(session: Session, limit: int = 100):
    return session.query(CustomerModel).limit(limit).all()


def create_customer(
    session: Session,
    name: str,
    is_ngo: bool = False,
    is_donor: bool = False,
    country: str = "GB",
    currency: str = "GBP",
) -> CustomerModel:
    customer = CustomerModel(
        name=name,
        is_ngo=is_ngo,
        is_donor=is_donor,
        country=country,
        currency=currency,
    )
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


def get_customers_by_ids(session: Session, customer_ids: list[UUID]):
    return session.query(CustomerModel).filter(CustomerModel.id.in_(customer_ids)).all()
