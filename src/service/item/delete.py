from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item

from src.repository.item.delete import delete_item_repository


async def delete_item_service(db: AsyncSession, item_to_delete: Item) -> None:
    await delete_item_repository(db, item_to_delete)