from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.item import ItemCreate, ItemRead, ItemUpdate
from src.db.session import get_async_session as get_db
from src.service.item.get_by_id import get_item_by_id_service
from src.api.dependencies import get_current_user_id 

router = APIRouter(prefix="/items", tags=["Items"])




@router.get("/{item_id}", response_model=ItemRead)
async def read_item_by_id(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _ = Depends(get_current_user_id) 
):
    item = await get_item_by_id_service(db, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item
