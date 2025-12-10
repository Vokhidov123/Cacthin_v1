from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.user.get_by_email import get_by_email
from src.core.security import verify_password
from src.schemas.user import UserCreate, UserUpdate
from src.models.user import User


async def authenticate(db: AsyncSession, email: str, password: str) -> User:
    user = await get_by_email(db, email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user
