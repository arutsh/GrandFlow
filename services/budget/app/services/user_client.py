import requests
from app.core.config import settings
from functools import lru_cache
import uuid


USER_SERVICE_URL = settings.user_service_url


class UserServiceError(Exception):
    pass


def get_user(user_id: str | uuid.UUID, token: str) -> dict:
    """
    Fetch a user from the user service by ID.
    """
    try:
        resp = requests.get(
            f"{USER_SERVICE_URL}{user_id}", headers={"Authorization": f"Bearer {token}"}
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        raise UserServiceError(f"Failed to fetch user {user_id}") from e


# cache frequent calls to reduce network requests
@lru_cache(maxsize=128)
def get_user_cached(user_id: str | uuid.UUID, token: str) -> dict:
    return get_user(user_id, token)


def get_valid_user(user_id: str | uuid.UUID, token: str) -> dict:

    user = get_user_cached(user_id, token)
    if not user:
        raise ValueError(f"User {user_id} not found")
    return user


def is_superuser(user_id: str | uuid.UUID, token: str) -> bool:
    user = get_user_cached(user_id, token)
    return user.get("role") == "superuser"


def get_user_customer_id(user_id: str | uuid.UUID, token: str) -> uuid.UUID | None:
    user = get_user_cached(user_id, token)
    return user.get("customer_id") if user else None
