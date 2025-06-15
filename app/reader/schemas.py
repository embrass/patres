from pydantic import BaseModel, EmailStr


class ReaderCreate(BaseModel):
    name: str

class ReaderResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True