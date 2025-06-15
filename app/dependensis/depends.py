from app.backend.db import async_session_maker
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_db():
    async with async_session_maker() as db:
        try:
            yield db
        finally:
            await db.close()


class TokenData(BaseModel):
    id: int


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            "weqdhygQUOYDQWDJocpdewkqodODkdq21",
            algorithms=["HS256"]
        )
        user_id: int = payload.get("sub")  # Получаем ID, а не email
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(id=user_id)
    except JWTError:
        raise credentials_exception


    from app.librarian.models import Librarian
    user = await db.execute(
        select(Librarian).where(Librarian.id == token_data.id)
    )
    user = user.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user
