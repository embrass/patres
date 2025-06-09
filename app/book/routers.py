from fastapi import APIRouter, FastAPI, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from app.book.models import Book
from app.book.schemas import BookCreate, BookResponse
from app.backend.db import async_session_maker
from typing import Optional



app = FastAPI()

router = APIRouter(
    prefix="/book",
    tags=["Books"]
)


async def get_db():
    async with async_session_maker() as db:  # Используем async with для автоматического управления сессией
        try:
            yield db
        finally:
            await db.close()




# CREATE - Создание новой книги
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


# READ (single) - Получение книги по ID
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



# UPDATE - Обновление информации о книге
@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
        book_id: int,
        book: BookCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        # Получаем книгу для обновления
        result = await db.execute(select(Book).where(Book.id == book_id))
        db_book = result.scalars().first()
        if db_book is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Книга не найдена"
            )

        # Проверяем уникальность ISBN, если он изменен
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


# DELETE - Удаление книги
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


# Дополнительный endpoint для поиска по автору
@router.get("/by-author/{author}", response_model=list[BookResponse])
async def get_books_by_author(author: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book).where(Book.author.ilike(f"%{author}%")))
    books = result.scalars().all()
    if not books:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книги данного автора не найдены"
        )
    return books