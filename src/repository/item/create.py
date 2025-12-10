# src/repository/item/create.py

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from src.schemas.item import ItemCreate


async def create(db: AsyncSession, item_obj: Item) -> Item:

    db.add(item_obj)
    await db.commit()
    await db.refresh(item_obj)
    return item_obj