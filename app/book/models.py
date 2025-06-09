from app.backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship



class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=True)
    isbn = Column(String, unique=True, nullable=True)
    copies_available = Column(Integer, default=1, nullable=False)
    copies = Column(Integer, default=1)

    borrows = relationship("Borrow", back_populates="book")






"""
   One or more mappers failed to initialize - can't proceed with initialization of other mappers. Triggering mapper: 'Mapper[Book(book)]'. 
   Original exception was: When initializing mapper Mapper[Book(book)], expression 'Borrow' failed to locate a name ('Borrow').
    If this is a class name, consider adding this relationship() to the <class 'app.book.models.Book'> class after both dependent classes have been defined."""