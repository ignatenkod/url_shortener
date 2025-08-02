from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
import uuid

from ...services.analytics import AnalyticsService
from ...services.security import rate_limiter
from ...utils.visualization import AnalyticsVisualizer
from ...database.session import get_async_session

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/url/{url_id}/stats")
async def get_url_stats(
    url_id: uuid.UUID,
    request: Request,
    time_range: int = 7,  # дни
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получает статистику кликов для URL
    
    - **url_id**: UUID URL
    - **time_range**: Диапазон в днях (по умолчанию 7)
    """
    # Проверка rate limit
    if not await rate_limiter.check_rate_limit(request):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    stats = await AnalyticsService.get_clicks_stats(
        db, 
        url_id, 
        timedelta(days=time_range)
    )
    return stats

@router.get("/url/{url_id}/clicks-plot")
async def get_clicks_plot(
    url_id: uuid.UUID,
    request: Request,
    time_range: int = 7,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Возвращает график кликов по странам
    
    - **url_id**: UUID URL
    - **time_range**: Диапазон в днях (по умолчанию 7)
    """
    if not await rate_limiter.check_rate_limit(request):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    stats = await AnalyticsService.get_clicks_stats(
        db, 
        url_id, 
        timedelta(days=time_range)
    
    plot_bytes = AnalyticsVisualizer.create_clicks_plot(
        stats["countries"],
        title=f"Клики по странам (последние {time_range} дней)"
    )
    
    return StreamingResponse(
        plot_bytes, 
        media_type="image/png",
        headers={"Cache-Control": "max-age=3600"}
    )

@router.get("/url/{url_id}/timeline-plot")
async def get_timeline_plot(
    url_id: uuid.UUID,
    request: Request,
    time_range: int = 7,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Возвращает график кликов по времени
    
    - **url_id**: UUID URL
    - **time_range**: Диапазон в днях (по умолчанию 7)
    """
    if not await rate_limiter.check_rate_limit(request):
        raise HTTPException(status_code=429, detail="Too many requests")
    
    # Здесь должна быть реализация получения данных по времени
    # Для примера используем фиктивные данные
    import random
    from datetime import datetime, timedelta
    
    timeline_data = {
        datetime.now() - timedelta(hours=i): random.randint(0, 20)
        for i in range(24 * time_range)
    }
    
    plot_bytes = AnalyticsVisualizer.create_timeline_plot(
        timeline_data,
        title=f"Клики по времени (последние {time_range} дней)"
    )
    
    return StreamingResponse(
        plot_bytes, 
        media_type="image/png",
        headers={"Cache-Control": "max-age=3600"}
    )
