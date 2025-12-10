from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.db.session import get_async_session as get_db
from src.api.dependencies import get_current_user_id 
from src.schemas.item import ItemCreate, ItemRead, ItemUpdate

from src.service.item.create import create_item_service 


router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_db),
    owner_id: int = Depends(get_current_user_id) 
):
    return await create_item_service(db=db, item_in=item_in, owner_id=owner_id)
