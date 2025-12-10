from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.user.get_by_id import get_by_id
from src.repository.user.delete import delete
from src.core.security import get_password_hash, verify_password
from src.schemas.user import UserCreate, UserUpdate
from src.models.user import User

async def delete(db: AsyncSession, user_id: int):
    user = await get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")

    await delete(db, user)
