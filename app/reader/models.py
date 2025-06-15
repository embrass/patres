
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.backend.db import Base
from typing import List


class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    borrow_records: Mapped[List["Borrow"]] = relationship("Borrow", back_populates="reader")