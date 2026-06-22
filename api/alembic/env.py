from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# para que encuentre app/
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import Base
import app.models  # importa todos los modelos

config = context.config

# leer variables de entorno
config.set_main_option("DB_USER", os.environ.get("POSTGRES_USER", "pos_user"))
config.set_main_option("DB_PASS", os.environ.get("POSTGRES_PASSWORD", "pos_password"))
config.set_main_option("DB_HOST", os.environ.get("POSTGRES_HOST", "db"))
config.set_main_option("DB_PORT", os.environ.get("POSTGRES_PORT", "5432"))
config.set_main_option("DB_NAME", os.environ.get("POSTGRES_DB", "pos_cafeteria"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
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
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()