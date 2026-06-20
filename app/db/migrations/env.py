from dotenv import load_dotenv
import os

from logging.config import fileConfig
from sqlalchemy import pool
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
# from app.models.pomiar import Base
from app.models.base_class import Base

load_dotenv()

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


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # 1. Pobierz URL
    app_mode = os.getenv("APP_MODE")
    db_url = os.environ.get("CONN_STR_DEV") if app_mode == 'DEV' else os.environ.get("CONN_STR_PROD")
    
    if not db_url:
        raise ValueError("Nie ustawiono zmiennej środowiskowej z adresem bazy danych!")

    # 2. Stwórz silnik asynchroniczny
    # Uwaga: jeśli używasz asyncpg, URL musi zaczynać się od postgresql+asyncpg://
    connectable = create_async_engine(
        db_url,
        poolclass=pool.NullPool,
    )

    # 3. Użyj asyncio.run, aby obsłużyć asynchroniczne połączenie
    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    def do_run_migrations(connection):
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(run_async_migrations())
    
    # Zamknij silnik po zakończeniu
    asyncio.run(connectable.dispose())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
