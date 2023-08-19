from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, DeclarativeMeta

from src.config import settings

DATABASE_URL = settings.database_url

Base: DeclarativeMeta = declarative_base()


async_engine = create_async_engine(DATABASE_URL)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
