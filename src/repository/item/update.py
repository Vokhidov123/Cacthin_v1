# src/repository/item/update.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError # Для обработки ошибок БД
from src.models.item import Item
from src.schemas.item import ItemUpdate


async def update_item_repository(db: AsyncSession, item: Item, item_update: ItemUpdate) -> Item:

    update_data = item_update.model_dump(exclude_unset=True) 

    for key, value in update_data.items():
        setattr(item, key, value)
    
    try:
        await db.commit()
        await db.refresh(item)
        return item
    except SQLAlchemyError as e:
        await db.rollback()
        raise e