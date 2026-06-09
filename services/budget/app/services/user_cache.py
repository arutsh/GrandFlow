from typing import Dict, Any, Optional
from uuid import UUID

import structlog

from app.db.session import SessionLocal
from app.models.user_cache import UserProfileModel
from app.services.user_client import get_user

logger = structlog.get_logger(__name__)


def get_user_from_cache(user_id: UUID) -> Optional[Dict[str, Any]]:
    session = SessionLocal()
    try:
        profile = session.query(UserProfileModel).filter(
            UserProfileModel.user_id == user_id
        ).first()

        if not profile:
            logger.debug("cache_miss", user_id=str(user_id))
            return None

        logger.debug("cache_hit", user_id=str(user_id))
        return {
            "id": str(profile.user_id),
            "email": profile.email,
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "status": profile.status,
            "customer_id": str(profile.customer_id) if profile.customer_id else None,
            "role": profile.role,
        }
    finally:
        session.close()


def get_user_from_cache_or_fallback(
    user_id: UUID, token: str
) -> Optional[Dict[str, Any]]:
    cached = get_user_from_cache(user_id)
    if cached:
        return cached

    logger.warning("cache_miss_fallback_attempted", user_id=str(user_id))

    try:
        user = get_user(str(user_id), token)

        session = SessionLocal()
        try:
            profile = session.query(UserProfileModel).filter(
                UserProfileModel.user_id == user_id
            ).first()

            if profile:
                profile.email = user.get("email")
                profile.first_name = user.get("first_name")
                profile.last_name = user.get("last_name")
                profile.status = user.get("status")
                profile.customer_id = (
                    UUID(user.get("customer_id"))
                    if user.get("customer_id")
                    else None
                )
                profile.role = user.get("role")
            else:
                profile = UserProfileModel(
                    user_id=user_id,
                    email=user.get("email"),
                    first_name=user.get("first_name"),
                    last_name=user.get("last_name"),
                    status=user.get("status"),
                    customer_id=(
                        UUID(user.get("customer_id"))
                        if user.get("customer_id")
                        else None
                    ),
                    role=user.get("role"),
                )
                session.add(profile)

            session.commit()
            logger.info("cache_populated_from_fallback", user_id=str(user_id))
        finally:
            session.close()

        return user
    except Exception as e:
        logger.error(
            "fallback_http_failed",
            user_id=str(user_id),
            error=str(e),
        )
        raise
