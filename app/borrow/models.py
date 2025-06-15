from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.backend.db import Base, engine



class Borrow(Base):
    __tablename__ = "borrows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(Integer, ForeignKey("books.id"))
    reader_id: Mapped[int] = mapped_column(Integer, ForeignKey("readers.id"))
    borrow_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    return_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    book: Mapped["Book"] = relationship("Book", back_populates="borrow_records")
    reader: Mapped["Reader"] = relationship("Reader", back_populates="borrow_records")






