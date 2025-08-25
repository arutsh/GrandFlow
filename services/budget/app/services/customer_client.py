import requests
from functools import lru_cache

CUSTOMER_SERVICE_URL = "http://users-service:8000/customers/"


class CustomerServiceError(Exception):
    pass


def get_customer(customer_id: str) -> dict:
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
def get_customer_cached(customer_id: str) -> dict:
    return get_customer(customer_id)


def validate_customer_type(customer_id: str, expected_type: str):
    customer = get_customer_cached(customer_id)
    if customer["type"] != expected_type:
        raise ValueError(f"Customer {customer_id} is not of type {expected_type}")
    return customer
