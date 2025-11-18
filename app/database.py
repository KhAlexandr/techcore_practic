from typing import AsyncGenerator

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession

engine = create_async_engine(
    "postgresql+asyncpg://fastapi_user:mysecretpassword@postgres_container:5432/fastapi2",
    echo=True,
)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
