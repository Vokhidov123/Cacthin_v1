from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from src.db.base import Base

from src.models.item import Item
from src.models.user import User

import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine # Убедитесь, что это импортировано

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

# src/db/migrations/env.py (ИСПРАВЛЕННАЯ ВЕРСИЯ)

# ... (импорты и настройки до run_migrations_online) ...

def run_migrations_online() -> None:
    """Run migrations in 'online' mode using AsyncEngine."""
    
    # ⚠️ Читаем конфигурацию синхронного Engine
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def run_async_migrations():
        async_connectable = AsyncEngine(connectable)

        async with async_connectable.connect() as connection:
            
            await connection.run_sync(
                lambda sync_connection: context.configure(
                    connection=sync_connection, 
                    target_metadata=target_metadata,
                    transactional_ddl=False, 
                )
            )

            await connection.run_sync(
                lambda sync_connection: context.run_migrations()
            )

    asyncio.run(run_async_migrations())


# if context.is_offline_mode():
#     run_migrations_offline()
# else:
run_migrations_online()