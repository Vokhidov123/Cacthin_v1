

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.user.get_by_email import get_by_email

from src.repository.user.create import create as create_in_repository 

from src.core.security import get_password_hash
from src.schemas.user import UserCreate
from src.models.user import User



async def create(db: AsyncSession, data: UserCreate) -> User:

    existing = await get_by_email(db, data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    
    user = User(
        email=data.email,
        hashed_password=get_password_hash(data.password)
    )

   
    return await create_in_repository(db, user)