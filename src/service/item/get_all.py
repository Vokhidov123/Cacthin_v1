from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from typing import List, Optional

from src.repository.item.get_all import get_all as get_all_repository


async def get_all_items_service(
    db: AsyncSession, 
    limit: int, 
    offset: int, 
    user_id: Optional[int]
) -> List[Item]:
    return await get_all_repository(db, limit, offset, user_id)