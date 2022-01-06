from motor.motor_asyncio import AsyncIOMotorClient

async_session = AsyncIOMotorClient(
        "localhost",
        maxPoolSize=10,
        minPoolSize=10,
        tz_aware=True,
    )
