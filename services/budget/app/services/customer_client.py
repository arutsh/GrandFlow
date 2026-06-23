import requests
from app.core.config import settings
from functools import lru_cache
import uuid
from app.core.exceptions import DomainError

CUSTOMER_SERVICE_URL = settings.customer_service_url


class CustomerServiceError(Exception):
    pass


def get_customer(customer_id: str | uuid.UUID) -> dict:
    try:
        resp = requests.get(f"{CUSTOMER_SERVICE_URL}{customer_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise CustomerServiceError(f"Failed to fetch customer {customer_id}") from e


@lru_cache(maxsize=128)
def get_customer_cached(customer_id: str | uuid.UUID) -> dict:
    return get_customer(customer_id)


def validate_customer_can_fund(customer_id: str | uuid.UUID, raise_domain_error: bool = False):
    """Assert the customer has is_donor=True (can issue grants)."""
    Error = DomainError if raise_domain_error else ValueError
    try:
        customer = get_customer_cached(customer_id)
    except CustomerServiceError as e:
        raise Error(str(e))

    if not customer.get("is_donor"):
        raise Error(f"Customer {customer_id} is not a donor and cannot fund budgets")
    return customer


def validate_customer_can_own(customer_id: str | uuid.UUID, raise_domain_error: bool = False):
    """Assert the customer has is_ngo=True (can receive grants / own budgets)."""
    Error = DomainError if raise_domain_error else ValueError
    try:
        customer = get_customer_cached(customer_id)
    except CustomerServiceError as e:
        raise Error(str(e))

    if not customer.get("is_ngo"):
        raise Error(f"Customer {customer_id} is not an NGO and cannot own budgets")
    return customer
