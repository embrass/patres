#uvicorn app.main:app --reload
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker

engine = create_async_engine('postgresql+asyncpg://phone:phone@localhost:5432/phone', echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

#alembic revision --autogenerate -m "Initial migration"