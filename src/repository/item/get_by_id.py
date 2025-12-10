# src/repository/item/get_by_id.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from typing import Optional


async def get_by_id(db: AsyncSession, item_id: int) -> Optional[Item]:

    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalars().first()