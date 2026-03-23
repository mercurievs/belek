"""
Lesson Repository
Репозиторий для работы с уроками
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.infrastructure.database.models import LessonModel
from app.domain.enums import EnglishLevel


class LessonRepository:
    """Репозиторий для работы с уроками"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(
        self, 
        title: str, 
        description: str, 
        level: EnglishLevel, 
        order: int,
        xp_reward: int = 50
    ) -> LessonModel:
        """Создать новый урок"""
        db_lesson = LessonModel(
            title=title,
            description=description,
            level=level,
            order=order,
            xp_reward=xp_reward,
            is_published=True
        )
        self.db.add(db_lesson)
        self.db.commit()
        self.db.refresh(db_lesson)
        return db_lesson
    
    def get_by_id(self, lesson_id: int) -> Optional[LessonModel]:
        """Получить урок по ID"""
        return self.db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    
    def get_by_level(self, level: EnglishLevel) -> List[LessonModel]:
        """Получить все уроки определённого уровня"""
        return (
            self.db.query(LessonModel)
            .filter(LessonModel.level == level, LessonModel.is_published == True)
            .order_by(LessonModel.order)
            .all()
        )
    
    def get_all_published(self, skip: int = 0, limit: int = 100) -> List[LessonModel]:
        """Получить все опубликованные уроки"""
        return (
            self.db.query(LessonModel)
            .filter(LessonModel.is_published == True)
            .order_by(LessonModel.level, LessonModel.order)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update(self, lesson_id: int, **kwargs) -> Optional[LessonModel]:
        """Обновить урок"""
        lesson = self.get_by_id(lesson_id)
        if lesson:
            for key, value in kwargs.items():
                if hasattr(lesson, key):
                    setattr(lesson, key, value)
            self.db.commit()
            self.db.refresh(lesson)
        return lesson
    
    def delete(self, lesson_id: int) -> bool:
        """Удалить урок"""
        lesson = self.get_by_id(lesson_id)
        if lesson:
            self.db.delete(lesson)
            self.db.commit()
            return True
        return False
