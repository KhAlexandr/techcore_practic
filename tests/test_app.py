import pytest

from fastapi.testclient import TestClient

from app.books.models import Book
from app.routers.books import BookRepository
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
        service.repo,
        "get_by_id",
        return_value=Book(id=1, title="Test", year=2025)
    )
    result = await service.get_book(1, mock_session)
    assert result.id == 1
    assert result.title == "Test"
    assert result.year == 2025


def test_endpoint():
    client = TestClient(app)
    response = client.get("/api/books")
    assert response.status_code == 200


def test_simple_add():
    assert 1 + 1 == 2
