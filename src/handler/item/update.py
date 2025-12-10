from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.session import get_async_session as get_db
from src.api.dependencies import get_current_user_id 
from src.schemas.item import ItemCreate, ItemRead, ItemUpdate

from src.service.item.get_by_id import get_item_by_id_service
from src.service.item.update import update_item_service 
router = APIRouter(prefix="/items", tags=["Items"])





@router.patch("/{item_id}", response_model=ItemRead)
async def update_item_handler(
    item_id: int,
    item_update: ItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    
    item = await get_item_by_id_service(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    if item.owner_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this item")
        
    return await update_item_service(db, item, item_update)
