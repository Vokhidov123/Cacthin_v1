from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List



from src.service.item.get_all import get_all_items_service 
from src.db.session import get_async_session as get_db
from src.api.dependencies import get_current_user_id 
from src.schemas.item import ItemCreate, ItemRead, ItemUpdate
from src.service.item.get_by_id import get_item_by_id_service

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("/", response_model=List[ItemRead])
async def read_all_items(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    owner_only: bool = Query(False, description="Если True, возвращает только элементы текущего пользователя"),
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id) 
):
    user_filter_id = current_user_id if owner_only else None
    
    return await get_all_items_service(
        db=db, 
        limit=limit, 
        offset=offset, 
        user_id=user_filter_id
    )
