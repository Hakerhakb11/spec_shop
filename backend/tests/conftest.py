import os

TEST_DATABASE_URL = (
    "postgresql+psycopg://test_shop_user:test_shop_password@localhost:5433/test_shop_db"
)
os.environ["POSTGRES_USER"] = "test_shop_user"
os.environ["POSTGRES_PASSWORD"] = "test_shop_password"
os.environ["POSTGRES_DB"] = "test_shop_db"
os.environ["POSTGRES_PORT"] = "5433"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.dependencies import get_async_db
from app.main import app

engine_test = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = async_sessionmaker(
    engine_test, expire_on_commit=False, autoflush=False
)


@pytest.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture(autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    async def override_get_async_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_async_db] = override_get_async_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
