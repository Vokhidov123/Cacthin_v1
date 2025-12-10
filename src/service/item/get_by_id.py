from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from typing import Optional


from src.repository.item.get_by_id import get_by_id as get_by_id_repository


async def get_item_by_id_service(db: AsyncSession, item_id: int) -> Optional[Item]:
 
    return await get_by_id_repository(db, item_id)