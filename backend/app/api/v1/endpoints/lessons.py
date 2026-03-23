"""
Lesson Endpoints
API endpoints для работы с уроками
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.infrastructure.database.base import get_db
from app.api.deps import get_current_user
from app.services.lesson_service import LessonService
from app.api.v1.schemas.lesson import LessonResponse, LessonDetailsResponse, StartLessonResponse
from app.domain.enums import EnglishLevel

router = APIRouter()


@router.get("/", response_model=List[LessonResponse])
def get_lessons(
    level: Optional[EnglishLevel] = Query(None, description="Фильтр по уровню"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить список всех уроков с прогрессом пользователя
    
    - **level**: Опциональный фильтр по уровню (A1, A2, B1, B2, C1)
    
    Требуется аутентификация
    """
    lesson_service = LessonService(db)
    
    lessons = lesson_service.get_all_lessons(
        user_id=current_user["id"],
        level=level
    )
    
    return lessons


@router.get("/{lesson_id}", response_model=LessonDetailsResponse)
def get_lesson_details(
    lesson_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить детальную информацию об уроке
    
    - **lesson_id**: ID урока
    
    Требуется аутентификация
    """
    lesson_service = LessonService(db)
    
    lesson = lesson_service.get_lesson_details(
        lesson_id=lesson_id,
        user_id=current_user["id"]
    )
    
    if lesson is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Урок не найден"
        )
    
    return lesson


@router.post("/{lesson_id}/start", response_model=StartLessonResponse)
def start_lesson(
    lesson_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Начать урок (изменить статус на "В процессе")
    
    - **lesson_id**: ID урока
    
    Требуется аутентификация
    """
    lesson_service = LessonService(db)
    
    try:
        result = lesson_service.start_lesson(
            user_id=current_user["id"],
            lesson_id=lesson_id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
