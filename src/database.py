from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import *
from typing import AsyncGenerator
from sqlalchemy import MetaData

engine=create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}",
    future=True,
    echo=True
)
SessionLocal=sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
Base=declarative_base()

metadata = MetaData()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session