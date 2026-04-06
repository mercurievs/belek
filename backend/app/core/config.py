"""
Конфигурация приложения
Загружает переменные окружения из .env файла
"""

import json
from typing import ClassVar, List
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """
    Настройки приложения
    Автоматически загружаются из .env файла
    """
    
    # Application
    APP_NAME: str = "English Learning Platform"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./english_learning.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    LOCAL_CORS_ORIGINS: ClassVar[List[str]] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    BACKEND_CORS_ORIGINS: List[str] = LOCAL_CORS_ORIGINS.copy()
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        """Преобразует строку CORS origins в список и добавляет локальные origin для разработки"""
        if isinstance(v, str):
            if v.startswith("["):
                parsed = json.loads(v)
            else:
                parsed = [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            parsed = v
        else:
            parsed = []

        # Сохраняем пользовательские origin, но всегда разрешаем локальную разработку.
        merged = parsed + cls.LOCAL_CORS_ORIGINS
        return list(dict.fromkeys(merged))
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создаём глобальный экземпляр настроек
settings = Settings()
