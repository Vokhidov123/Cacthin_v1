from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from src.schemas.item import ItemUpdate
from src.repository.item.update import update_item_repository


async def update_item_service(
    db: AsyncSession, 
    item_to_update: Item, 
    item_update_data: ItemUpdate
) -> Item:

    return await update_item_repository(db, item_to_update, item_update_data)