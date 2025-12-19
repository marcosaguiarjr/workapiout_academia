import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection  # Importação correta para o do_run_migrations
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# --- IMPORTANTE: Apontar para o seu BaseModel ---
from workout_api.contrib.models import BaseModel
# Importe os modelos para garantir que o SQLAlchemy os registre no MetaData
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- AJUSTE AQUI: Metadata que contém suas tabelas ---
target_metadata = BaseModel.metadata

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

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    # Aqui usamos o async with que corrigimos anteriormente
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    # Forma mais robusta de rodar o loop assíncrono no Windows
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()