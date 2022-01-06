import asyncio
import pprint
from typing import Generator

import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from sqlmodel import SQLModel

from tests.database import engine

pytest_plugins = ["tests.fixtures"]


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()

    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture()
async def motor():
    async_session = AsyncIOMotorClient(
        "localhost",
        maxPoolSize=10,
        minPoolSize=10,
        tz_aware=True,
    )
    session = async_session.get_database("testing")
    return session


@pytest.fixture
async def app(event_loop) -> Generator:
    app = {}

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
        yield app
        await conn.run_sync(SQLModel.metadata.drop_all)
