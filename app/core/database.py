
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.core.config import settings
from typing import AsyncGenerator

engine = create_async_engine(settings.DB_URL, future=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False) # Фабрика session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:    # Анотация, являктся ассинхронным генератором.
    async with async_session_maker() as session:
        yield session
    """
    Инъекция зависимости - это одна из зависимостей.
    Чтобы не дублировался код:    async with async_session_maker() as session:
    """

session = get_async_session()

