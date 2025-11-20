from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.books.models import Book
from app.database import Base


@pytest.fixture(autouse=True)
def mock_kafka():
    with patch("app.kafka_conf.producer.AIOKafkaProducer") as mock_producer:
        mock_instance = AsyncMock()
        mock_producer.return_value = mock_instance
        mock_instance.start = AsyncMock()
        mock_instance.stop = AsyncMock()
        mock_instance.send_and_wait = AsyncMock()
        yield


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
