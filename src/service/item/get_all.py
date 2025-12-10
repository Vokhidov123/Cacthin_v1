from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from typing import List

from src.repository.item.get_all import get_all as get_all_repository


async def get_all_items_service(db: AsyncSession) -> List[Item]:
    return await get_all_repository(db)