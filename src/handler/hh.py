from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# Импорт ваших зависимостей
from src.db.session import get_db  # Или как у вас называется получение сессии
from src.schemas.user import UserCreate, UserRead, UserUpdate
from src.schemas.token import Token, UserLogin # Схемы, которые мы определили выше
from src.core.security import create_access_token
from src.api.dependencies import get_current_user_id

# Импорт вашей бизнес-логики (функций, которые вы скинули)
# Предполагаем, что они лежат в src/services/user.py или аналогичном месте
from service.user.create import create as create_user_service
from service.user.authenticate import authenticate as authenticate_user_service
from service.user.delete import delete as delete_user_service
from service.user.update import update as update_user_service
from src.repository.user.get_by_id import get_by_id # Напрямую репозиторий для GET запросов

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Регистрация нового пользователя.
    """
    return await create_user_service(db, user_in)



@router.post("/login", response_model=Token)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
 
    user = await authenticate_user_service(db, login_data.email, login_data.password)
    
  
    access_token = create_access_token(subject=str(user.id))
    
    return Token(access_token=access_token)



@router.get("/me", response_model=UserRead)
async def read_users_me(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id) 
):
   
    user = await get_by_id(db, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.patch("/me", response_model=UserRead)
async def update_user_me(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
   
    return await update_user_service(db, user_id, user_update)



@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(
    db: AsyncSession = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    await delete_user_service(db, user_id)
    return None