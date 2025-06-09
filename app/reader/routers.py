"""from fastapi import APIRouter, HTTPException, status, Response
from app.librarian.auth import get_password_hash
from app.reader.dao import ReaderDAO
from app.reader.schemas import SUserReg
from app.librarian.auth import authenticate_user
from app.librarian.auth import create_access_token

router = APIRouter(
    prefix="/reader",
    tags=["Auth&User"]
)


@router.post("/register")
async def register_user(user_data: SUserReg):
    existing_user = await ReaderDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=401)
    hashed_password = get_password_hash(user_data.password)
    await ReaderDAO.insert_data(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserReg):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

"""