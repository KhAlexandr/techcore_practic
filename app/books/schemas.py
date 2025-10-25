from pydantic import BaseModel


class BasBookScheme(BaseModel):
    title: str
    year: int | None = None


class BookScheme(BasBookScheme):
    author_id: int
