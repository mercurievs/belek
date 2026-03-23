"""
API v1 Router
Объединяет все endpoints версии 1
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, lessons, exercises, admin

# Создаём главный роутер для API v1
api_router = APIRouter()

# Подключаем роутеры endpoints
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    lessons.router,
    prefix="/lessons",
    tags=["Lessons"]
)

api_router.include_router(
    exercises.router,
    prefix="/exercises",
    tags=["Exercises"]
)

api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["Admin"]
)
