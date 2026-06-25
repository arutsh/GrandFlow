from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_provider import AIProvider


async def get_by_name(name: str, db: AsyncSession) -> AIProvider | None:
    result = await db.execute(
        select(AIProvider).where(AIProvider.name == name, AIProvider.is_active.is_(True))
    )
    return result.scalar_one_or_none()


async def list_active(db: AsyncSession) -> list[AIProvider]:
    result = await db.execute(
        select(AIProvider).where(AIProvider.is_active.is_(True)).order_by(AIProvider.name)
    )
    return list(result.scalars().all())
