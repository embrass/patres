from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.dependensis.depends import get_db
from app.book.models import Book
from app.book.schemas import BookCreate, BookResponse


app = FastAPI()

router = APIRouter(
    prefix="/book",
    tags=["Books"]
)


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    try:
        if book.isbn:
            result = await db.execute(select(Book).where(Book.isbn == book.isbn))
            existing_book = result.scalars().first()
            if existing_book:
                raise HTTPException(
                    status_code=400,
                    detail="Книга с таким ISBN уже существует"
                )

        db_book = Book(**book.dict())
        db.add(db_book)
        await db.commit()
        await db.refresh(db_book)
        return db_book
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{book_id}", response_model=BookResponse)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalars().first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )
    return db_book


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
        book_id: int,
        book: BookCreate,
        db: AsyncSession = Depends(get_db)
):
    try:

        result = await db.execute(select(Book).where(Book.id == book_id))
        db_book = result.scalars().first()
        if db_book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Книга не найдена"
            )


        if book.isbn and book.isbn != db_book.isbn:
            result = await db.execute(select(Book).where(Book.isbn == book.isbn))
            existing_book = result.scalars().first()
            if existing_book:
                raise HTTPException(
                    status_code=400,
                    detail="Книга с таким ISBN уже существует"
                )



        updated_book = result.scalars().first()
        return updated_book
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.id == book_id))
    db_book = result.scalars().first()
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    await db.execute(delete(Book).where(Book.id == book_id))
    await db.commit()
    return {"ok": True}


