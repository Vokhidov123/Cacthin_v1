# src/schemas/item.py
from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_available: bool = True

class ItemCreate(ItemBase):
    pass 

class ItemUpdate(ItemBase):
   
    name: Optional[str] = None 
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None

class ItemRead(ItemBase):
    id: int
    owner_id: int 
    
    class Config:
        from_attributes = True