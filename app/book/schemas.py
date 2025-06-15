from pydantic import BaseModel, Field
from typing import Optional


class BookCreate(BaseModel):
    title: str
    author: str
    publication_year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int = Field(ge=0, default=1)


class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True

