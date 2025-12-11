from sqlalchemy import String, Boolean, event
from sqlalchemy.orm import Mapped, mapped_column, attributes
from src.db.base import Base, TimestampMixin

class User(TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

@event.listens_for(User, 'before_insert', retval=True)
@event.listens_for(User, 'before_update', retval=True)
def user_before_persist(mapper, connection, target):

    if target.email and attributes.instance_state(target).modified_event(target, 'email'):
        target.email = target.email.lower().strip()
    
    return False