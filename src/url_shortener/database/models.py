import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from .base import Base

class URL(Base):
    """Модель для хранения сокращенных URL"""
    __tablename__ = "urls"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(String(2048), nullable=False)
    short_key = Column(String(32), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        return f"<URL(short_key='{self.short_key}')>"

class Click(Base):
    """Модель для хранения данных о кликах"""
    __tablename__ = "clicks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url_id = Column(UUID(as_uuid=True), ForeignKey("urls.id"), nullable=False)
    clicked_at = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    referrer = Column(String(2048))
    country = Column(String(2))
    device_type = Column(String(50))
    browser = Column(String(50))
    os = Column(String(50))

    def __repr__(self):
        return f"<Click(url_id='{self.url_id}', clicked_at='{self.clicked_at}')>"
