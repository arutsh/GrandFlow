from uuid import uuid4


def make_valid_user(user_id=None, customer_id=None, role="user", token="testtoken"):
    """Returns a dict matching the structure of get_validated_user() output:
    the decoded JWT payload with an added 'token' key."""
    return {
        "user_id": str(user_id or uuid4()),
        "customer_id": str(customer_id or uuid4()),
        "role": role,
        "token": token,
    }
