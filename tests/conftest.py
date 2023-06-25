import pytest_asyncio
import asyncio
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.pool import NullPool
from httpx import AsyncClient

from src.config import *
from src.database import Base
from src.main import app

#pytest tests --asyncio-mode=auto -v
engine_test=create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}test",    
    poolclass=NullPool
)
SessionLocal_test=sessionmaker(bind=engine_test, expire_on_commit=False, class_=AsyncSession)
Base.metadata.bind = engine_test

async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal_test() as session:
        yield session

app.dependency_overrides["get_async_session"] = get_async_session_test
        
@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        
@pytest_asyncio.fixture(scope='session')
def event_loop(request):
    #create an instance of the default event loop for each test case
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
    
client = TestClient(app)

@pytest_asyncio.fixture(scope="session")
async def ac():
    async with AsyncClient(app=app, base_url="http://localhost:8000/") as ac:
        yield ac