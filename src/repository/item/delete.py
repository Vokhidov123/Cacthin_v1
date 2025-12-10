# src/repository/item/delete.py

from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item


async def delete_item_repository(db: AsyncSession, item: Item) -> None:

    await db.delete(item)
    await db.commit()