from pydantic import BaseModel


class BookScheme(BaseModel):
    title: str
    year: int | None = None
