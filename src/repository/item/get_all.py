# src/repository/item/get_all.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from typing import List


async def get_all(db: AsyncSession) -> List[Item]:


    result = await db.execute(select(Item).order_by(Item.id))
    return result.scalars().all()