# ЧАСТЬ РОУТЕРА ДЛЯ РЕГИСТРАЦИИ

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_async_session as get_db # 💡 Исправление: Используем правильное имя с псевдонимом
from src.schemas.user import UserCreate, UserRead
from src.service.user.create import create as create_user_service # Ваш сервисный слой

# Предполагаем, что переменная router объявлена в главном файле роутера
router = APIRouter(prefix="/users", tags=["Users"]) 

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрация нового пользователя.
    """
    # Вызов сервисного слоя для создания пользователя
    return await create_user_service(db, user_in)