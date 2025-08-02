from datetime import timedelta
import redis.asyncio as redis
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..config import settings

class RateLimiter:
    """Сервис для ограничения количества запросов"""
    
    def __init__(self):
        self.redis = None
        
    async def init_redis(self):
        """Инициализация подключения к Redis"""
        self.redis = redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_db,
            decode_responses=True
        )
    
    async def check_rate_limit(self, request: Request, user_id: str = None) -> bool:
        """
        Проверяет не превышен ли лимит запросов
        
        Args:
            request: Объект запроса FastAPI
            user_id: Идентификатор пользователя (опционально)
            
        Returns:
            bool: True если лимит не превышен
        """
        if not self.redis:
            await self.init_redis()
        
        # Используем IP или user_id для идентификации
        key = user_id or request.client.host
        current = await self.redis.get(key)
        
        if current and int(current) > settings.rate_limit:
            return False
            
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, settings.rate_limit_period)
        await pipe.execute()
        return True

rate_limiter = RateLimiter()
