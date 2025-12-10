from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User



async def update(db: AsyncSession, user: User) -> User:
    await db.commit()
    await db.refresh(user)
    return user