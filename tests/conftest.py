from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.core.config import settings
from typing import AsyncGenerator
import pytest_asyncio
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient

from app.core.database import get_async_session
from app.main import app
from app.models.base import Base


test_engine = create_async_engine(settings.TEST_DB_URL, future=True, poolclass=NullPool,)
test_async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)

async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest_asyncio.fixture(scope='session')
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest_asyncio.fixture(scope="session",
                loop_scope="session",
                autouse=True)
async def prepare_test_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

@pytest_asyncio.fixture(autouse=True)
async def clean_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield

    await test_engine.dispose()