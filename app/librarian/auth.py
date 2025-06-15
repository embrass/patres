from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.librarian.models import Librarian

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, "weqdhygQUOYDQWDJocpdewkqodODkdq21", "HS256"
    )
    return encoded_jwt

async def authenticate_liberian(email: str, password: str, db: AsyncSession) -> Optional[Librarian]:
    result = await db.execute(
        select(Librarian).where(Librarian.email == email)
    )
    liberian = result.scalar_one_or_none()
    if not liberian or not pwd_context.verify(password, liberian.password):
        return None
    return liberian


