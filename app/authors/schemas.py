from pydantic import BaseModel


class AuthorScheme(BaseModel):
    first_name: str
    last_name: str
    age: int | None = None
