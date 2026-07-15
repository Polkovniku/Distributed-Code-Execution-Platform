from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(url=settings.database_url, echo=False)

AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False) 

class Base(DeclarativeBase):
    pass