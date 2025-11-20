import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.books.models import Book
from app.main import app
from app.routers.books import BookRepository, get_db_session


class BookService:
    def __init__(self):
        self.repo = BookRepository()

    async def get_book(self, id: int, session):
        return await self.repo.get_by_id(id, session=session)


@pytest.mark.asyncio
async def test_get_book(mocker):
    service = BookService()
    mock_session = mocker.Mock()

    mocker.patch.object(
        service.repo, "get_by_id", return_value=Book(id=1, title="Test", year=2025)
    )
    result = await service.get_book(1, mock_session)
    assert result.id == 1
    assert result.title == "Test"
    assert result.year == 2025


@pytest.mark.asyncio
async def test_endpoint(mock_db_session):
    app.dependency_overrides[get_db_session] = lambda: mock_db_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=False
    ) as ac:
        response = await ac.get("/api/books/")
        assert response.status_code == 200
        books = response.json()
        assert len(books["books"]) == 10
    app.dependency_overrides.clear()


def test_validation():
    client = TestClient(app)
    response = client.post("/api/books", json={"title": 123, "year": 5})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_e2e_real_db_async(postgres_container):
    original_url = postgres_container.get_connection_url()
    async_db_url = original_url.replace(
        "postgresql+psycopg2://", "postgresql+asyncpg://"
    )
    async_engine = create_async_engine(async_db_url)

    async with async_engine.begin() as conn:
        await conn.execute(
            text(
                """
            CREATE TABLE authors (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(50),
                last_name VARCHAR(50),
                age INTEGER
            )
        """
            )
        )
        await conn.execute(
            text(
                """
            CREATE TABLE books (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                year INTEGER,
                author_id INTEGER REFERENCES authors(id)
            )
        """
            )
        )
        await conn.execute(
            text(
                "INSERT INTO authors (id, first_name, last_name, age) VALUES (1, 'Test', 'Author', 30)"  # noqa
            )
        )

    session_maker = async_sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )
    app.dependency_overrides[get_db_session] = lambda: session_maker()
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", follow_redirects=False
    ) as ac:
        response = await ac.get("/api/books/")
        assert response.status_code == 200
        response_create = await ac.post(
            "/api/books/", json={"title": "Bio", "year": 5, "author_id": 1}
        )
        assert response_create.status_code == 201
    app.dependency_overrides.clear()
