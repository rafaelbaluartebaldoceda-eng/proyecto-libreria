"""Configuracion de entorno para ejecutar migraciones Alembic."""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from database.connection import get_database_url, get_driver_connect_args
from database.orm_models import Base


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", str(get_database_url()))

target_metadata = Base.metadata


def run_migrations_offline():
    """Ejecuta migraciones en modo offline."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Ejecuta migraciones en modo online usando el engine del proyecto."""
    connectable = create_engine(
        "postgresql+psycopg2://",
        connect_args=get_driver_connect_args(),
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
