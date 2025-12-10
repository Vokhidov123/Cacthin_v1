from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.security import get_password_hash
from src.repository.user.get_by_id import get_by_id
from src.schemas.user import UserCreate, UserUpdate
from src.models.user import User
from src.repository.user.update import update as update_1

async def update(db: AsyncSession, user_id: int, data: UserUpdate) -> User:
    user = await get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not found")

    update_data = data.dict(exclude_unset=True)

    if "password" in update_data:
        user.hashed_password = get_password_hash(update_data.pop("password"))

    for key, value in update_data.items():
        setattr(user, key, value)

    return await update_1(db, user)