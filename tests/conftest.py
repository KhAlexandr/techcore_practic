import pytest

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database import Base
from app.books.models import Book


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def mock_db_session(mocker):
    session = mocker.AsyncMock(spec=AsyncSession)

    mock_scalars = mocker.Mock()

    mock_scalars.all.return_value = [
        Book(id=i, title="Test", year=2025) for i in range(1, 11)
    ]
    session.scalars.return_value = mock_scalars

    return session


@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer() as pg:
        yield pg
