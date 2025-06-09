#uvicorn app.main:app --reload
from fastapi import FastAPI
from app.librarian.routers import router as router_librarian
from app.book.routers import router as router_books

app = FastAPI()

app.include_router(router_books)
app.include_router(router_librarian)


