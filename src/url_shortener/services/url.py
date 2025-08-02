import uuid
from typing import Optional
from nanoid import generate
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import URL
from ..schemas.url import URLCreate, URLInDB
from .keygen import generate_short_key

class URLService:
    """Сервис для работы с сокращенными URL"""
    
    @staticmethod
    async def create_url(
        db: AsyncSession, 
        url: URLCreate,
        custom_key: Optional[str] = None
    ) -> URLInDB:
        """
        Создает новую запись сокращенного URL
        
        Args:
            db: Асинхронная сессия БД
            url: Схема с оригинальным URL
            custom_key: Пользовательский ключ (опционально)
            
        Returns:
            URLInDB: Схема с информацией о созданном URL
        """
        short_key = custom_key or generate_short_key()
        db_url = URL(
            original_url=str(url.original_url),
            short_key=short_key
        )
        db.add(db_url)
        await db.commit()
        await db.refresh(db_url)
        return URLInDB.from_orm(db_url)

    @staticmethod
    async def get_url_by_key(
        db: AsyncSession, 
        short_key: str
    ) -> Optional[URLInDB]:
        """
        Получает оригинальный URL по короткому ключу
        
        Args:
            db: Асинхронная сессия БД
            short_key: Короткий ключ URL
            
        Returns:
            Optional[URLInDB]: Схема с информацией о URL или None
        """
        result = await db.execute(
            select(URL).where(URL.short_key == short_key, URL.is_active == True)
        )
        db_url = result.scalar_one_or_none()
        return URLInDB.from_orm(db_url) if db_url else None

    @staticmethod
    async def deactivate_url(
        db: AsyncSession, 
        url_id: uuid.UUID
    ) -> bool:
        """
        Деактивирует URL
        
        Args:
            db: Асинхронная сессия БД
            url_id: UUID URL
            
        Returns:
            bool: True если операция успешна
        """
        await db.execute(
            update(URL)
            .where(URL.id == url_id)
            .values(is_active=False)
        )
        await db.commit()
        return True
