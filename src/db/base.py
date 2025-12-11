from datetime import datetime, timezone # <<< ИМПОРТИРУЕМ timezone ИЗ datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, DateTime

class Base(DeclarativeBase):
    pass


class TimestampMixin:

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)