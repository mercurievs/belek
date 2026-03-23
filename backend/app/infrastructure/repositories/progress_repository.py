"""
Progress Repository
Репозиторий для работы с прогрессом пользователей
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.models import UserProgressModel, ExerciseResultModel
from app.domain.enums import LessonStatus


class ProgressRepository:
    """Репозиторий для работы с прогрессом пользователей"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_progress(
        self, 
        user_id: int, 
        lesson_id: int,
        exercises_total: int = 0
    ) -> UserProgressModel:
        """
        Получить или создать прогресс пользователя по уроку
        
        Args:
            user_id: ID пользователя
            lesson_id: ID урока
            exercises_total: Общее количество упражнений в уроке
        
        Returns:
            Модель прогресса
        """
        progress = (
            self.db.query(UserProgressModel)
            .filter(
                UserProgressModel.user_id == user_id,
                UserProgressModel.lesson_id == lesson_id
            )
            .first()
        )
        
        if not progress:
            progress = UserProgressModel(
                user_id=user_id,
                lesson_id=lesson_id,
                status=LessonStatus.NOT_STARTED,
                xp_earned=0,
                exercises_completed=0,
                exercises_total=exercises_total
            )
            self.db.add(progress)
            self.db.commit()
            self.db.refresh(progress)
        
        return progress
    
    def start_lesson(self, user_id: int, lesson_id: int) -> UserProgressModel:
        """Начать урок (изменить статус на IN_PROGRESS)"""
        progress = self.get_or_create_progress(user_id, lesson_id)
        if progress.status == LessonStatus.NOT_STARTED:
            progress.status = LessonStatus.IN_PROGRESS
            progress.started_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(progress)
        return progress
    
    def complete_exercise(
        self, 
        user_id: int, 
        lesson_id: int, 
        xp_earned: int
    ) -> UserProgressModel:
        """
        Отметить завершение упражнения
        
        Args:
            user_id: ID пользователя
            lesson_id: ID урока
            xp_earned: Заработано XP за упражнение
        
        Returns:
            Обновлённый прогресс
        """
        progress = self.get_or_create_progress(user_id, lesson_id)
        progress.exercises_completed += 1
        progress.xp_earned += xp_earned
        
        # Если все упражнения выполнены, завершить урок
        if progress.exercises_completed >= progress.exercises_total:
            progress.status = LessonStatus.COMPLETED
            progress.completed_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(progress)
        return progress
    
    def get_user_progress(self, user_id: int) -> List[UserProgressModel]:
        """Получить весь прогресс пользователя"""
        return (
            self.db.query(UserProgressModel)
            .filter(UserProgressModel.user_id == user_id)
            .all()
        )
    
    def save_exercise_result(
        self,
        user_id: int,
        exercise_id: int,
        user_answer: str,
        is_correct: bool,
        xp_earned: int
    ) -> ExerciseResultModel:
        """
        Сохранить результат выполнения упражнения
        
        Args:
            user_id: ID пользователя
            exercise_id: ID упражнения
            user_answer: Ответ пользователя
            is_correct: Правильный ли ответ
            xp_earned: Заработано XP
        
        Returns:
            Модель результата
        """
        result = ExerciseResultModel(
            user_id=user_id,
            exercise_id=exercise_id,
            user_answer=user_answer,
            is_correct=is_correct,
            xp_earned=xp_earned
        )
        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)
        return result
