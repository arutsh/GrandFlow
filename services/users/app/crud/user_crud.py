from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user import UserModel
from app.utils.security import hash_password
from app.services.event_publisher import get_publisher


from app.core.logging import get_logger

logger = get_logger(__name__)


def _user_event_payload(user: UserModel) -> dict:
    return {
        "user_id": str(user.id),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "status": user.status,
        "customer_id": str(user.customer_id) if user.customer_id else None,
        "role": user.role,
    }


async def _publish_user_event(event_type: str, user: UserModel) -> None:
    try:
        publisher = get_publisher()
        await publisher.publish(event_type, _user_event_payload(user))
    except Exception as e:
        logger.error(
            "user_event_publish_failed", event_type=event_type, user_id=str(user.id), error=str(e)
        )


def get_user(session: Session, user_id: UUID):
    return session.query(UserModel).filter(UserModel.id == user_id).first()


def get_user_by_email(session: Session, email: str):
    return session.query(UserModel).filter(UserModel.email == email).first()


def is_superuser(session: Session, user_id: UUID) -> bool:
    user = get_user(session, user_id)
    return user is not None and user.role == "superuser"


def get_users_query(session: Session, user_ids: list[UUID] | None = None):
    query = session.query(UserModel)
    if user_ids:
        query = query.filter(UserModel.id.in_(user_ids))
    return query


def get_users_by_ids(session: Session, user_ids: list[UUID]):
    return get_users_query(session, user_ids).all()


def get_users(session: Session, limit: int = 100):
    return get_users_query(session).limit(limit).all()


async def create_user(
    session: Session,
    email: str,
    password: str,
    first_name: str | None = "",
    last_name: str | None = "",
    role: str | None = "user",
    customer_id: UUID | None = None,
) -> UserModel:
    existing = session.query(UserModel).filter(UserModel.email == email).first()
    if existing:
        logger.warning("user_creation_rejected", email=email, reason="email_already_exists")
        raise ValueError("Email already registered")

    user = UserModel(
        email=email,
        hashed_password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        role=role,
        customer_id=customer_id,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    logger.info(
        "user_created",
        user_id=str(user.id),
        email=user.email,
        role=role,
        customer_id=str(customer_id) if customer_id else None,
    )

    await _publish_user_event("user.created", user)
    return user


async def update_user(session: Session, user: UserModel, updates: dict) -> UserModel:
    for key, value in updates.items():
        if key == "password":
            value = hash_password(value)
        setattr(user, key, value)

    session.commit()
    session.refresh(user)

    await _publish_user_event("user.updated", user)
    return user


def get_user_customer_id(session: Session, user_id: UUID) -> UUID | None:
    user = get_user(session, user_id)
    if user:
        return user.customer_id
    return None
