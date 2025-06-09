from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=100)
    publication_year: Optional[int] = Field(None, ge=0, le=datetime.now().year)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    copies_available: int = Field(1, ge=0)

    @validator('isbn')
    def isbn_must_be_valid(cls, v):
        if v is not None and not v.replace("-", "").isalnum():
            raise ValueError('ISBN должен содержать только буквы, цифры и дефисы')
        return v


class BookResponse(BookCreate):
    id: int

    class Config:
        from_attributes = True


