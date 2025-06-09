from sqlalchemy import Column, Integer, String
from app.backend.db import Base


class Librarian(Base):
    __tablename__ = "librarian"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)