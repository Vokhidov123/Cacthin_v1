from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.session import get_async_session as get_db
from src.api.dependencies import get_current_user_id 
from src.schemas.item import ItemCreate, ItemRead, ItemUpdate
from src.service.item.get_by_id import get_item_by_id_service
from src.service.item.delete import delete_item_service

router = APIRouter(prefix="/items", tags=["Items"])





@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item_handler( # Переименовал
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    
    item = await get_item_by_id_service(db, item_id)
    if not item:
        return

    if item.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this item")
        
    await delete_item_service(db, item) # Передаем объект Item в сервис
    return