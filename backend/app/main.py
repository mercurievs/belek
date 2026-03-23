"""
FastAPI Application Entry Point
Главный файл приложения - точка входа для backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router
from app.infrastructure.database.base import Base, engine

# Создаём таблицы в БД (в продакшене используйте Alembic миграции)
Base.metadata.create_all(bind=engine)

# Создаём FastAPI приложение
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend для платформы изучения английского языка",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Настройка CORS - ДОЛЖНА БЫТЬ ДО ВКЛЮЧЕНИЯ РОУТЕРОВ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Временно разрешаем все origins для отладки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Подключаем роутеры API
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
def root():
    """
    Корневой endpoint
    Проверка работоспособности API
    """
    return {
        "message": "English Learning Platform API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint
    Для мониторинга состояния сервера
    """
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


# Для запуска в режиме разработки
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Автоперезагрузка при изменении кода
    )
