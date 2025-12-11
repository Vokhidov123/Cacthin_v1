from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.item import Item
from typing import List, Optional


async def get_all(
    db: AsyncSession, 
    limit: int, 
    offset: int, 
    user_id: Optional[int]
) -> List[Item]:
    
    query = select(Item).order_by(Item.id)

    if user_id is not None:
        query = query.filter(Item.owner_id == user_id)

    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    return result.scalars().all()