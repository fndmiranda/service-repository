from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URI = "sqlite+aiosqlite:///./tests/testing.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URI, future=True, echo=True)
async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
