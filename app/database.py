from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


engine = create_async_engine(
    "postgresql+asyncpg://fastapi_user:mysecretpassword@localhost:5432"
    "/fastapi")

session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
