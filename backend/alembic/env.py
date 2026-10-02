from logging.config import fileConfig
import asyncio
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from app.core.database import Base, AsyncSessionLocal
from app.models.vehicle import Vehicle, Location, Company, User
from app.models.reservation import Customer, Reservation, Extra, ReservationExtra, PricingRule
from app.models.assistant import Conversation, Message, Review, AuditLog

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Use the models' metadata for autogenerate support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    # Use the async engine from our database config
    from app.core.database import engine

    # For Alembic to work with AsyncConnection, we use the run_sync method
    # to call the synchronous migration logic.
    async with engine.begin() as conn:
        await conn.run_sync(do_run_migrations)

def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    # Alembic's online mode normally expects a synchronous function.
    # We wrap the async function in asyncio.run.
    asyncio.run(run_migrations_online())
