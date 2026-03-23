"""
Pydantic Schemas for Exercises
"""

from pydantic import BaseModel, Field
from typing import Optional, List

from app.domain.enums import ExerciseType, DifficultyLevel


class ExerciseBase(BaseModel):
    """Базовая схема упражнения"""
    type: ExerciseType = Field(..., description="Тип упражнения")
    question: str = Field(..., description="Текст вопроса")
    difficulty: DifficultyLevel = Field(DifficultyLevel.MEDIUM, description="Сложность")
    xp_reward: int = Field(10, description="Награда в XP")


class ExerciseCreate(ExerciseBase):
    """Схема для создания упражнения"""
    lesson_id: int
    correct_answer: str
    options: Optional[List[str]] = None
    explanation: Optional[str] = None
    order: int = 0


class ExerciseResponse(ExerciseBase):
    """Схема ответа с данными упражнения (БЕЗ правильного ответа)"""
    id: int
    options: Optional[List[str]] = None
    explanation: Optional[str] = None
    audio_url: Optional[str] = None
    
    class Config:
        from_attributes = True


class SubmitAnswerRequest(BaseModel):
    """Схема для отправки ответа на упражнение"""
    exercise_id: Optional[int] = Field(None, description="ID упражнения")
    lesson_id: Optional[int] = Field(None, description="ID урока")
    user_answer: str = Field(..., description="Ответ пользователя")


class ProgressInfo(BaseModel):
    """Информация о прогрессе"""
    exercises_completed: int
    exercises_total: int
    lesson_completed: bool


class SubmitAnswerResponse(BaseModel):
    """Схема ответа на проверку упражнения"""
    is_correct: bool = Field(..., description="Правильный ли ответ")
    correct_answer: Optional[str] = Field(None, description="Правильный ответ (если неправильно)")
    explanation: Optional[str] = Field(None, description="Объяснение (если неправильно)")
    xp_earned: int = Field(..., description="Заработано XP")
    new_total_xp: int = Field(..., description="Новое общее количество XP")
    progress: ProgressInfo = Field(..., description="Прогресс урока")
