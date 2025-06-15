from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.backend.db import Base



class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    publication_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    isbn: Mapped[str | None] = mapped_column(String, unique=True, nullable=True)
    copies: Mapped[int] = mapped_column(Integer, default=1)
    copies_available: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    borrow_records: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="book")



