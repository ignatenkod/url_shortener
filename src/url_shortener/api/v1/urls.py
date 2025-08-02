from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from ...schemas.url import URLCreate, URLInfo
from ...services.url import URLService
from ...services.analytics import AnalyticsService
from ...database.session import get_async_session

router = APIRouter(prefix="/urls", tags=["urls"])

@router.post("/", response_model=URLInfo)
async def create_short_url(
    url: URLCreate,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Создает короткий URL
    
    - **original_url**: Оригинальный длинный URL
    """
    try:
        db_url = await URLService.create_url(db, url)
        return db_url
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{short_key}", response_model=URLInfo)
async def get_url_info(
    short_key: str,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Получает информацию о коротком URL
    
    - **short_key**: Короткий идентификатор URL
    """
    db_url = await URLService.get_url_by_key(db, short_key)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return db_url

@router.get("/{short_key}/redirect")
async def redirect_url(
    short_key: str,
    request: Request,
    db: AsyncSession = Depends(get_async_session)
):
    """
    Перенаправляет на оригинальный URL по короткому ключу
    
    - **short_key**: Короткий идентификатор URL
    """
    db_url = await URLService.get_url_by_key(db, short_key)
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    
    # Логируем клик
    await AnalyticsService.create_click(
        db,
        ClickCreate(url_id=db_url.id),
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent")
    )
    
    return RedirectResponse(url=db_url.original_url)
