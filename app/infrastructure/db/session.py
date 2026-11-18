import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "POSTGRES_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/layer_db",
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)