from fastapi import APIRouter, HTTPException, status, Response
from app.librarian.auth import get_password_hash

#from app.reader.schemas import SUserReg
from app.librarian.schemas import LibrarianCreate
from app.librarian.auth import authenticate_liberian
from app.librarian.auth import create_access_token
from app.librarian.dao import RegLibrarian
router = APIRouter(
    prefix="/auth",
    tags=["Auth&User"]
)


@router.post("/register")
async def register_liberian(user_data: LibrarianCreate):
    existing_liberian = await RegLibrarian.find_one_or_none(email=user_data.email)
    if existing_liberian:
        raise HTTPException(status_code=401)
    hashed_password = get_password_hash(user_data.password)
    await RegLibrarian.insert_data(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_liberian(response: Response, user_data: LibrarianCreate):
    liberian = await authenticate_liberian(user_data.email, user_data.password)
    if not liberian:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    access_token = create_access_token({"sub": liberian.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

