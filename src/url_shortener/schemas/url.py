from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import Optional

class URLBase(BaseModel):
    """Базовая схема для URL"""
    original_url: HttpUrl

class URLCreate(URLBase):
    """Схема для создания нового URL"""
    pass

class URLInfo(URLBase):
    """Схема с информацией о URL"""
    short_key: str
    is_active: bool
    created_at: datetime
    clicks_count: int = 0

    class Config:
        orm_mode = True

class URLInDB(URLInfo):
    """Схема для URL из БД"""
    id: str
