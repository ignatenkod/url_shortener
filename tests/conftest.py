import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.url_shortener.main import app
from src.url_shortener.database.base import Base
from src.url_shortener.database.session import async_engine
from src.url_shortener.config import settings

@pytest.fixture(scope="session")
async def test_db():
    # Создаем тестовую БД
    test_engine = create_async_engine(
        f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@"
        f"{settings.postgres_server}:{settings.postgres_port}/test_{settings.postgres_db}"
    )
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield test_engine
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()

@pytest.fixture
async def db_session(test_db):
    # Создаем сессию для каждого теста
    async_session = sessionmaker(
        test_db, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session

@pytest.fixture
async def client(db_session):
    # Переопределяем зависимость в приложении
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_async_session] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()
