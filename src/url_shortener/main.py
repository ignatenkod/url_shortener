from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api.v1.urls import router as url_router

app = FastAPI(
    title="URL Shortener",
    description="Сервис сокращения URL с аналитикой",
    version="0.1.0",
    root_path=settings.root_path if hasattr(settings, "root_path") else ""
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(url_router)

@app.on_event("startup")
async def startup():
    """Действия при запуске приложения"""
    pass

@app.on_event("shutdown")
async def shutdown():
    """Действия при остановке приложения"""
    pass
