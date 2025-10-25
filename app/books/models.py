from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[int | None] = None

    # author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    #
    # author: Mapped["Author"] = relationship("Author", back_populates="books")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            # "author_id": self.author_id,
        }
