#uvicorn app.main:app --reload
from fastapi import FastAPI
from app.librarian.routers import router as router_librarian
from app.book.routers import router as router_books
from app.reader.routers import router as router_reader
from app.borrow.routers import router as router_borrow
app = FastAPI()

app.include_router(router_books)
app.include_router(router_librarian)
app.include_router(router_reader)
app.include_router(router_borrow)

# git push -f -u origin main