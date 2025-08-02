from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .base import Base
from ..config import settings

# Настройка асинхронного движка SQLAlchemy
async_engine = create_async_engine(
    f"postgresql+asyncpg://{settings.postgres_user}:{settings.postgres_password}@"
    f"{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db}",
    echo=settings.app_debug,
    pool_size=20,
    max_overflow=0
)

# Фабрика асинхронных сессий
async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

async def get_async_session() -> AsyncSession:
    """Генератор асинхронных сессий для зависимостей FastAPI"""
    async with async_session_maker() as session:
        yield session
