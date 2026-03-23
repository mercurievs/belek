"""
Exercise Endpoints
API endpoints для работы с упражнениями
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database.base import get_db
from app.api.deps import get_current_user
from app.services.exercise_service import ExerciseService
from app.api.v1.schemas.exercise import (
    ExerciseResponse, 
    SubmitAnswerRequest, 
    SubmitAnswerResponse
)

router = APIRouter()


@router.get("", response_model=List[ExerciseResponse])
def get_all_exercises(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить все упражнения для практики
    
    Требуется аутентификация
    
    Примечание: Правильные ответы НЕ возвращаются в ответе
    """
    exercise_service = ExerciseService(db)
    exercises = exercise_service.get_all_exercises()
    return exercises


@router.get("/{exercise_id}", response_model=ExerciseResponse)
def get_exercise_by_id(
    exercise_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить упражнение по ID
    
    - **exercise_id**: ID упражнения
    
    Требуется аутентификация
    """
    exercise_service = ExerciseService(db)
    exercise = exercise_service.get_exercise_by_id(exercise_id)
    
    if not exercise:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Упражнение не найдено"
        )
    
    return exercise


@router.get("/lesson/{lesson_id}", response_model=List[ExerciseResponse])
def get_lesson_exercises(
    lesson_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить все упражнения урока
    
    - **lesson_id**: ID урока
    
    Требуется аутентификация
    
    Примечание: Правильные ответы НЕ возвращаются в ответе
    """
    exercise_service = ExerciseService(db)
    
    exercises = exercise_service.get_lesson_exercises(lesson_id)
    
    return exercises


@router.post("/{exercise_id}/submit", response_model=SubmitAnswerResponse)
def submit_exercise_answer(
    exercise_id: int,
    answer_data: SubmitAnswerRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Отправить ответ на упражнение для проверки (новый формат для практики)
    
    - **exercise_id**: ID упражнения (из URL)
    - **user_answer**: Ответ пользователя
    
    Требуется аутентификация
    """
    exercise_service = ExerciseService(db)
    
    try:
        # Получаем упражнение для определения lesson_id
        exercise = exercise_service.get_exercise_by_id(exercise_id)
        if not exercise:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Упражнение не найдено"
            )
        
        result = exercise_service.submit_answer(
            user_id=current_user["id"],
            exercise_id=exercise_id,
            lesson_id=exercise["lesson_id"],
            user_answer=answer_data.user_answer
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.post("/submit", response_model=SubmitAnswerResponse)
def submit_answer(
    answer_data: SubmitAnswerRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Отправить ответ на упражнение для проверки
    
    - **exercise_id**: ID упражнения
    - **lesson_id**: ID урока
    - **user_answer**: Ответ пользователя
    
    Требуется аутентификация
    
    Бизнес-логика:
    1. Проверяется правильность ответа
    2. Начисляется XP если ответ правильный
    3. Обновляется прогресс урока
    4. Возвращается результат с объяснением (если неправильно)
    """
    exercise_service = ExerciseService(db)
    
    try:
        result = exercise_service.submit_answer(
            user_id=current_user["id"],
            exercise_id=answer_data.exercise_id,
            lesson_id=answer_data.lesson_id,
            user_answer=answer_data.user_answer
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
