from app.core.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from typing import AsyncIterator
from sqlalchemy.exc import SQLAlchemyError
import traceback


DATABASE_URI = str(get_settings().DATABASE_URI)

engine = create_async_engine(DATABASE_URI, echo=True, future=True)
AsyncLocalSession = sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# Dependency
async def get_session() -> AsyncIterator[sessionmaker]:
    try:
        yield AsyncLocalSession()
    except SQLAlchemyError as e:
        print(traceback.print_exc())