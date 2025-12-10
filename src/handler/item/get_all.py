from fastapi import APIRouter, Depends, status, HTTPException
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
    db: AsyncSession = Depends(get_db),
    _ = Depends(get_current_user_id) 
):

    return await get_all_items_service(db)
