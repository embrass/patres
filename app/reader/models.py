from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.backend.db import Base



class Reader(Base):
    __tablename__ = "reader"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    borrows = relationship("Borrow", back_populates="reader")

