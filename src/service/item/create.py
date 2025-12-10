

from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.item import ItemCreate, ItemRead
from src.models.item import Item


from src.repository.item.create import create as create_in_repository


async def create_item_service(
    db: AsyncSession, 
    item_in: ItemCreate, 
    owner_id: int
) -> Item:
   
    item_obj = Item(
        **item_in.model_dump(), 
        owner_id=owner_id
    )
    
    return await create_in_repository(db, item_obj)