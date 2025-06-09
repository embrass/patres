from app.backend.db import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime



class Borrow(Base):
    __tablename__ = "borrow"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("reader.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column(DateTime, nullable=True)

    books = relationship("Book", back_populates="borrows")
    readers = relationship("Reader", back_populates="borrow")



"""
When initializing mapper Mapper[Book(book)], expression 'Borrow' failed to locate a name ('Borrow'). If this is a class name,
consider adding this relationship() to the <class 'app.book.models.Book'> class after both dependent classes have been defined."""