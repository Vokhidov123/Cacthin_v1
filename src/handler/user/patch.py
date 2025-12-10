# ЧАСТЬ РОУТЕРА ДЛЯ ОБНОВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session as get_db 
from src.schemas.user import UserRead, UserUpdate
from src.service.user.update import update as update_user_service 
from src.api.dependencies import get_current_user_id 


router = APIRouter(prefix="/users", tags=["Users"]) 

@router.patch("/me", response_model=UserRead)
async def update_user_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Обновление данных текущего пользователя.
    """
    # Вызов сервисного слоя для обновления пользователя
    return await update_user_service(db, user_id, user_update)