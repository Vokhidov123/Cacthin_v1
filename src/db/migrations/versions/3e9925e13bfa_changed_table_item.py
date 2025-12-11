"""Changed table Item

Revision ID: 3e9925e13bfa
Revises: 9ab0820b150d
Create Date: 2025-12-11 13:30:35.519072

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3e9925e13bfa'
down_revision: Union[str, Sequence[str], None] = '9ab0820b150d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    # 1. Добавляем столбец как NULLABLE (чтобы не было ошибки при создании)
    op.add_column('items', sa.Column('characteristics', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    
    # 2. Заполняем существующие записи пустым словарем
    op.execute("UPDATE items SET characteristics = '{}'::jsonb WHERE characteristics IS NULL")
    
    # 3. Теперь меняем на NOT NULL
    # ВАЖНО: Здесь используется type_ вместо existing_type, чтобы исправить вашу ошибку
    op.alter_column('items', 'characteristics',
               type_=postgresql.JSONB(astext_type=sa.Text()),
               nullable=False,
               postgresql_using="characteristics::jsonb" 
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('items', 'characteristics')