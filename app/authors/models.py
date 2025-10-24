from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from app.database import Base


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    age: Mapped[int | None] = None
