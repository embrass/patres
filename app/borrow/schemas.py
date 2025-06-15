from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class BorrowBase(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[datetime]
class BorrowCreate(BorrowBase):
    pass

class BorrowResponse(BorrowBase):
    id: int
    borrow_date: datetime
    return_date: Optional[datetime] = None

class BorrowBookRequest(BaseModel):
    book_id: int
    reader_id: int

class ReturnBookRequest(BaseModel):
    borrow_id: int

    class Config:
        from_attributes = True
