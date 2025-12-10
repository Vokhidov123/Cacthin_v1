# src/repository/item/update.py

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from src.schemas.item import ItemUpdate


async def update_item_repository(db: AsyncSession, item: Item, item_update: ItemUpdate) -> Item:

    update_data = item_update.model_dump(exclude_unset=True) 

    for key, value in update_data.items():
        setattr(item, key, value)
    
    await db.commit()
    await db.refresh(item)
    return item