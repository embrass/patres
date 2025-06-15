from pydantic import BaseModel, EmailStr


class LibrarianCreate(BaseModel):
    email: EmailStr
    password: str


class LibrarianResponse(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True
