from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User



async def get_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalars().first()