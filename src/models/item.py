from sqlalchemy import String, Float, Boolean, ForeignKey, Index, JSON
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
import sqlalchemy as sa
from src.db.base import Base, TimestampMixin
from typing import Optional, List, Dict, Any

class Item(TimestampMixin, Base):
    __tablename__ = "items"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True) 
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    characteristics: Mapped[Dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default={}
    )
    
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    search_vector: Mapped[str] = mapped_column(
        TSVECTOR,
        sa.Computed(
            "to_tsvector('english', name || ' ' || coalesce(description, ''))", 
            persisted=True
        )
    )

Index(
    'idx_item_search_vector',
    Item.search_vector,
    postgresql_using='gin'
)