import asyncio
from typing import Generator

import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

pytest_plugins = ["tests.fixtures"]


@pytest_asyncio.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()

    try:
        yield loop
    finally:
        loop.close()


@pytest_asyncio.fixture()
async def motor():
    client = AsyncIOMotorClient(
        "localhost",
        maxPoolSize=10,
        minPoolSize=10,
        tz_aware=True,
    )
    await client.drop_database("testing")
    session = client.get_database("testing")
    yield session


@pytest_asyncio.fixture()
async def sqlalchemy():
    SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./tests/testing.db"

    engine = create_async_engine(
        SQLALCHEMY_DATABASE_URI, future=True, echo=True
    )
    async_session = sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield async_session
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def app(event_loop) -> Generator:
    app = {}
    yield app
