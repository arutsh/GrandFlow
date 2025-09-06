import requests
from app.core.config import settings
from functools import lru_cache
import uuid

CUSTOMER_SERVICE_URL = settings.customer_service_url


class CustomerServiceError(Exception):
    pass


def get_customer(customer_id: str | uuid.UUID) -> dict:
    """
    Fetch a customer from the customer service by ID.
    """
    try:
        resp = requests.get(f"{CUSTOMER_SERVICE_URL}{customer_id}")
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise CustomerServiceError(f"Failed to fetch customer {customer_id}") from e


# cache frequent calls to reduce network requests
@lru_cache(maxsize=128)
def get_customer_cached(customer_id: str | uuid.UUID) -> dict:
    return get_customer(customer_id)


def validate_customer_type(customer_id: str | uuid.UUID, expected_type: str):
    customer = get_customer_cached(customer_id)
    if customer["type"] != expected_type:
        raise ValueError(f"Customer {customer_id} is not of type {expected_type}")
    return customer
