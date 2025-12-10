from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User

async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    res = await db.execute(select(User).where(User.id == user_id))
    return res.scalars().first()