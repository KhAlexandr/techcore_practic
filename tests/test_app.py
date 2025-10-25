from app.books.models import Book


def test_simple_add():
    assert 1 + 1 == 2


def test_create_book(db_session):
    book = Book(title="Test", year=2025)
    db_session.add(book)
    db_session.commit()
