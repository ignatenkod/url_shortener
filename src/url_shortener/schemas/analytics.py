from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ClickBase(BaseModel):
    """Базовая схема для клика"""
    url_id: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class ClickCreate(ClickBase):
    """Схема для создания записи о клике"""
    pass

class ClickInfo(ClickBase):
    """Схема с информацией о клике"""
    id: str
    clicked_at: datetime
    country: Optional[str] = None
    device_type: Optional[str] = None
    browser: Optional[str] = None
    os: Optional[str] = None

    class Config:
        orm_mode = True
