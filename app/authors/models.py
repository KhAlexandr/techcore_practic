from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List

from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int | None] = None

    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")
