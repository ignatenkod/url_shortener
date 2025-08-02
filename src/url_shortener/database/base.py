from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass

Base = declarative_base(cls=Base)
