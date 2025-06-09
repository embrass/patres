from pydantic import BaseModel, EmailStr


class SUserReg(BaseModel):
    email: EmailStr
    password: str



class ReaderBase(BaseModel):
    name: str

class ReaderCreate(ReaderBase):
    pass

class Reader(ReaderBase):
    id: int
    class Config:
        orm_mode = True