from uuid import UUID
from sqlalchemy.orm import Session

from app.models.user import UserModel
from app.utils.security import hash_password


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


def create_user(
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
    return user


def update_user(session: Session, user: UserModel, updates: dict):
    for key, value in updates.items():
        if key == "password":
            value = hash_password(value)
        setattr(user, key, value)

    session.commit()
    session.refresh(user)
    return user


def get_user_customer_id(session: Session, user_id: UUID) -> UUID | None:
    user = get_user(session, user_id)
    if user:
        return user.customer_id
    return None
