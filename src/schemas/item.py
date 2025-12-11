from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ItemCharacteristics(BaseModel):
    weight_g: Optional[int] = None
    color: Optional[str] = None
    features: List[str] = []
    custom_params: Dict[str, Any] = {}
    
    class Config:
        extra = "allow"

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    is_available: bool = True

class ItemCreate(ItemBase):
    characteristics: ItemCharacteristics = Field(default_factory=ItemCharacteristics)


class ItemUpdate(ItemBase):
    
    name: Optional[str] = None 
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    is_available: Optional[bool] = None
    
    characteristics: Optional[ItemCharacteristics] = None

class ItemRead(ItemBase):
    id: int
    owner_id: int 
    characteristics: Optional[ItemCharacteristics] = None
    
    class Config:
        from_attributes = True
