from app.librarian.auth import get_password_hash
from fastapi import APIRouter, HTTPException, status, Response
from app.librarian.schemas import LibrarianCreate
from app.librarian.auth import authenticate_liberian, create_access_token, verify_password
from app.librarian.dao import RegLibrarian

from app.dependensis.depends import Depends, get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(

    tags=["Auth&Lib"]
)

@router.post("/register")
async def register_liberian(user_data: LibrarianCreate):
    existing_liberian = await RegLibrarian.find_one_or_none(email=user_data.email)
    if existing_liberian:
        raise HTTPException(status_code=401)
    hashed_password = get_password_hash(user_data.password)
    await RegLibrarian.insert_data(email=user_data.email, hashed_password=hashed_password)

@router.post("/token")
async def login_liberian(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    liberian = await authenticate_liberian(
        email=form_data.username,
        password=form_data.password,
        db=db
    )

    if not liberian:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token({"sub": liberian.id})
    return {"access_token": access_token, "token_type": "bearer"}

