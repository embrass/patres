from sqlalchemy import select, update, func
from fastapi import Depends, HTTPException, APIRouter

from app.dependensis.depends import get_current_user, get_db
from app.reader.schemas import ReaderResponse, ReaderCreate
from app.reader.models import Reader
from app.book.schemas import BookResponse
from app.book.models import Book
from app.borrow.models import Borrow
from app.borrow.schemas import BorrowBookRequest, ReturnBookRequest
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/reader",
    tags=["Readers"]
)



@router.post("/create/", response_model=ReaderResponse)
async def create_reader(reader: ReaderCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_reader = Reader(**reader.dict())
        db.add(db_reader)
        await db.commit()
        await db.refresh(db_reader)
        return db_reader
    except:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already exists")


@router.get("/readers/", response_model=list[ReaderResponse])
async def get_readers(db: AsyncSession = Depends(get_db), _: dict = Depends(get_current_user)):
    result = await db.execute(select(Reader))
    return result.scalars().all()


@router.get("/books/", response_model=list[BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Book))
    return result.scalars().all()



@router.post("/borrow/")
async def borrow_book(borrow: BorrowBookRequest, db: AsyncSession = Depends(get_db),
                      _: dict = Depends(get_current_user)):
    # Проверка доступности книги
    book = (await db.execute(select(Book).where(Book.id == borrow.book_id))).scalar_one_or_none()
    if not book or book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book not available")


    borrowed_count = (await db.execute(
        select(func.count()).where(
            Borrow.reader_id == borrow.reader_id,
            Borrow.return_date.is_(None)
        )
    )).scalar()
    if borrowed_count >= 3:
        raise HTTPException(status_code=400, detail="Reader has reached the limit (3 books)")


    borrowed_book = Borrow(**borrow.dict())
    db.add(borrowed_book)
    await db.execute(
        update(Book)
        .where(Book.id == borrow.book_id)
        .values(available_copies=Book.available_copies - 1)
    )
    await db.commit()
    return {"message": "Book borrowed successfully"}


# ===== Возврат книги =====
@router.post("/return/")
async def return_book(return_req: ReturnBookRequest, db: AsyncSession = Depends(get_db),
                      _: dict = Depends(get_current_user)):
    # Получаем запись о выдаче
    borrowed = (await db.execute(
        select(Borrow)
        .where(Borrow.id == return_req.borrow_id)
    )).scalar_one_or_none()

    if not borrowed or borrowed.return_date is not None:
        raise HTTPException(status_code=400, detail="Invalid borrow record")


    borrowed.return_date = func.now()
    await db.execute(
        update(Book)
        .where(Book.id == borrowed.book_id)
        .values(available_copies=Book.available_copies + 1)
    )
    await db.commit()
    return {"message": "Book returned successfully"}


@router.get("/reader-books/{reader_id}", response_model=list[BookResponse])
async def get_reader_books(reader_id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(get_current_user)):

    borrowed_books = (await db.execute(
        select(Borrow.book_id)
        .where(
            Borrow.reader_id == reader_id,
            Borrow.return_date.is_(None)
        )
    )).scalars().all()

    if borrowed_books:
        result = await db.execute(select(Book).where(Book.id.in_(borrowed_books)))
        return result.scalars().all()
    return []


