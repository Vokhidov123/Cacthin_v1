# ЧАСТЬ РОУТЕРА ДЛЯ УДАЛЕНИЯ ПОЛЬЗОВАТЕЛЯ

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_async_session as get_db # Использование псевдонима
from src.service.user.delete import delete as delete_user_service 
from src.api.dependencies import get_current_user_id 


router = APIRouter(prefix="/users", tags=["Users"]) 

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    """
    Удаление своего аккаунта.
    """
    # Вызов сервисного слоя для удаления пользователя
    await delete_user_service(db, user_id)
    # Возвращаем 204 No Content (None) после успешного удаления
    return None