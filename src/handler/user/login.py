# ЧАСТЬ РОУТЕРА ДЛЯ ЛОГИНА

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session as get_db # Использование псевдонима
from src.schemas.token import Token, UserLogin
from src.core.security import create_access_token 
from src.service.user.authenticate import authenticate as authenticate_user_service


router = APIRouter(prefix="/users", tags=["Users"]) 

@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Аутентификация и выдача JWT токена.
    """
    # 1. Проверяем учетные данные с помощью сервисного слоя
    user = await authenticate_user_service(db, login_data.email, login_data.password)
    
    # 2. Создаем токен: ID пользователя используется как 'subject' в токене
    access_token = create_access_token(subject=str(user.id))
    
    return Token(access_token=access_token)