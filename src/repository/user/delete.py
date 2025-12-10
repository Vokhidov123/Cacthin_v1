from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User



async def delete(db: AsyncSession, user: User) -> None:
    await db.delete(user)
    await db.commit()