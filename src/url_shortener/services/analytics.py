import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from user_agents import parse

from ..database.models import Click
from ..schemas.analytics import ClickCreate, ClickInfo
from ..utils.geoip import get_geoip_data

class AnalyticsService:
    """Сервис для работы с аналитикой кликов"""

    @staticmethod
    async def create_click(
        db: AsyncSession,
        click: ClickCreate,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> ClickInfo:
        """
        Создает запись о клике
        
        Args:
            db: Асинхронная сессия БД
            click: Данные клика
            ip_address: IP адрес пользователя
            user_agent: User-Agent строка
            
        Returns:
            ClickInfo: Информация о созданном клике
        """
        # Парсим User-Agent
        ua = parse(user_agent) if user_agent else None
        
        # Получаем геоданные
        geo_data = get_geoip_data(ip_address) if ip_address else None
        
        # Создаем запись в БД
        db_click = Click(
            url_id=click.url_id,
            ip_address=ip_address,
            user_agent=user_agent,
            country=geo_data.country.iso_code if geo_data and geo_data.country else None,
            device_type=ua.device.family if ua else None,
            browser=ua.browser.family if ua else None,
            os=ua.os.family if ua else None
        )
        
        db.add(db_click)
        await db.commit()
        await db.refresh(db_click)
        return ClickInfo.from_orm(db_click)

    @staticmethod
    async def get_clicks_stats(
        db: AsyncSession,
        url_id: uuid.UUID,
        time_range: Optional[timedelta] = None
    ) -> dict:
        """
        Возвращает статистику кликов для URL
        
        Args:
            db: Асинхронная сессия БД
            url_id: UUID URL
            time_range: Временной диапазон (опционально)
            
        Returns:
            dict: Статистика кликов
        """
        # Базовый запрос
        query = select(Click).where(Click.url_id == url_id)
        
        # Применяем временной фильтр если нужно
        if time_range:
            time_threshold = datetime.utcnow() - time_range
            query = query.where(Click.clicked_at >= time_threshold)
        
        # Получаем общее количество кликов
        total = await db.scalar(
            select(func.count()).select_from(query.subquery())
        
        # Группировка по странам
        countries = await db.execute(
            select(Click.country, func.count(Click.country))
            .where(Click.url_id == url_id)
            .group_by(Click.country)
        )
        countries_stats = dict(countries.all())
        
        return {
            "total_clicks": total or 0,
            "countries": countries_stats,
            "time_range": str(time_range) if time_range else "all_time"
        }
