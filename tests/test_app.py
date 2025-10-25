import pytest
from httpx import AsyncClient, ASGITransport

from fastapi.testclient import TestClient

from app.books.models import Book
from app.routers.books import BookRepository, get_db_session
from app.main import app


class BookService:
    def __init__(self):
        self.repo = BookRepository()

    def get_book(self, id: int, session):
        return self.repo.get_by_id(id, session=session)


@pytest.mark.asyncio
async def test_get_book(mocker):
    service = BookService()
    mock_session = mocker.Mock()

    mock_get = mocker.patch.object(
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
        transport=ASGITransport(app=app),
        base_url="http://test",
        follow_redirects=False
    ) as ac:
        response = await ac.get("/api/books/")
        assert response.status_code == 200
        books = response.json()
        assert len(books["books"]) == 10
    app.dependency_overrides.clear()


def test_validation():
    client = TestClient(app)
    response = client.post(
        "/api/books",
        json={"title": 123, "year": 5}
    )
    assert response.status_code == 422
