from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_provider_key import UserProviderKey


async def get_key(user_id: str, provider_id: str, db: AsyncSession) -> UserProviderKey | None:
    result = await db.execute(
        select(UserProviderKey).where(
            UserProviderKey.user_id == user_id,
            UserProviderKey.provider_id == provider_id,
        )
    )
    return result.scalar_one_or_none()


async def get_active_key(user_id: str, db: AsyncSession) -> UserProviderKey | None:
    """Return the first active BYOK key for this user (provider joined)."""
    result = await db.execute(
        select(UserProviderKey).where(
            UserProviderKey.user_id == user_id,
            UserProviderKey.encrypted_key.isnot(None),
        )
    )
    return result.scalar_one_or_none()


async def upsert_key(
    user_id: str,
    provider_id: str,
    encrypted_key: str | None,
    model_name: str | None,
    base_url: str | None,
    db: AsyncSession,
) -> UserProviderKey:
    now = datetime.now(timezone.utc)
    existing = await get_key(user_id, provider_id, db)
    if existing:
        existing.encrypted_key = encrypted_key
        existing.model_name = model_name
        existing.base_url = base_url
        existing.updated_at = now
        await db.commit()
        await db.refresh(existing)
        return existing
    row = UserProviderKey(
        user_id=user_id,
        provider_id=provider_id,
        encrypted_key=encrypted_key,
        model_name=model_name,
        base_url=base_url,
        created_at=now,
        updated_at=now,
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def delete_key(user_id: str, provider_id: str, db: AsyncSession) -> None:
    existing = await get_key(user_id, provider_id, db)
    if existing:
        existing.encrypted_key = None
        existing.updated_at = datetime.now(timezone.utc)
        await db.commit()
