from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app import settings


engine = create_async_engine(settings.ASYNC_DB_DSN)
session_local = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    # create new session
    async with session_local() as session:
        yield session
