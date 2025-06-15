
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.backend.db import Base


class Librarian(Base):
    __tablename__ = "librarian"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
