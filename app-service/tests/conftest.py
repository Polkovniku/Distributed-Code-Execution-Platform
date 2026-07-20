import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from main import app
from core.database import Base
from core.dependencies import get_db

TEST_DATABASE_URL = "postgresql+asyncpg://petrovich:password@localhost:5433/test_db"

test_engine = create_async_engine(url=TEST_DATABASE_URL, poolclass=NullPool)

TestSessionLocal = async_sessionmaker(bind=test_engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
        
    async with TestSessionLocal() as db:
        yield db
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session
        
    app.dependency_overrides[get_db] = override_get_db
    
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
    

@pytest_asyncio.fixture(scope="function")
async def user_data():
    return {
        "username": "testuser",
        "email": "test@gmail.com",
        "password": "passwordtest"
    }

        
@pytest_asyncio.fixture(scope="function")
async def auth_token(client: AsyncClient, user_data: dict):
    await client.post("/auth/register", json=user_data)
    response = await client.post(
        "/auth/login", 
        json={"email": user_data["email"], "password": user_data["password"]})
    return response.json()["access_token"]