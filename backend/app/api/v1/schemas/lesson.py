"""
Pydantic Schemas for Lessons
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from app.domain.enums import EnglishLevel, LessonStatus


class LessonBase(BaseModel):
    """Базовая схема урока"""
    title: str = Field(..., description="Название урока")
    description: Optional[str] = Field(None, description="Описание урока")
    level: EnglishLevel = Field(..., description="Уровень английского")
    order: int = Field(..., description="Порядковый номер урока")
    xp_reward: int = Field(50, description="Награда в XP за прохождение")


class LessonCreate(LessonBase):
    """Схема для создания урока"""
    pass


class LessonProgressInfo(BaseModel):
    """Информация о прогрессе урока"""
    status: LessonStatus
    exercises_completed: int
    exercises_total: int
    xp_earned: int


class LessonResponse(LessonBase):
    """Схема ответа с данными урока"""
    id: int
    progress: Optional[LessonProgressInfo] = None
    
    class Config:
        from_attributes = True


class LessonDetailsResponse(LessonResponse):
    """Детальная информация об уроке"""
    exercises_count: int
    
    class Config:
        from_attributes = True


class StartLessonResponse(BaseModel):
    """Ответ при начале урока"""
    lesson_id: int
    status: LessonStatus
    exercises_total: int
