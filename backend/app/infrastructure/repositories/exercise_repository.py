"""
Exercise Repository
Репозиторий для работы с упражнениями
"""

from typing import Optional, List
from sqlalchemy.orm import Session
import json

from app.infrastructure.database.models import ExerciseModel
from app.domain.enums import ExerciseType, DifficultyLevel


class ExerciseRepository:
    """Репозиторий для работы с упражнениями"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(
        self,
        lesson_id: int,
        type: ExerciseType,
        question: str,
        correct_answer: str,
        options: List[str] = None,
        difficulty: DifficultyLevel = DifficultyLevel.MEDIUM,
        xp_reward: int = 10,
        explanation: str = "",
        order: int = 0
    ) -> ExerciseModel:
        """Создать новое упражнение"""
        db_exercise = ExerciseModel(
            lesson_id=lesson_id,
            type=type,
            question=question,
            correct_answer=correct_answer,
            options=json.dumps(options) if options else None,
            difficulty=difficulty,
            xp_reward=xp_reward,
            explanation=explanation,
            order=order
        )
        self.db.add(db_exercise)
        self.db.commit()
        self.db.refresh(db_exercise)
        return db_exercise
    
    def get_by_id(self, exercise_id: int) -> Optional[ExerciseModel]:
        """Получить упражнение по ID"""
        return self.db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()
    
    def get_all(self) -> List[ExerciseModel]:
        """Получить все упражнения"""
        return self.db.query(ExerciseModel).order_by(ExerciseModel.order).all()
    
    def get_by_lesson_id(self, lesson_id: int) -> List[ExerciseModel]:
        """Получить все упражнения урока"""
        return (
            self.db.query(ExerciseModel)
            .filter(ExerciseModel.lesson_id == lesson_id)
            .order_by(ExerciseModel.order)
            .all()
        )
    
    def get_options(self, exercise: ExerciseModel) -> Optional[List[str]]:
        """Получить варианты ответов (для multiple choice)"""
        if exercise.options:
            return json.loads(exercise.options)
        return None
    
    def delete(self, exercise_id: int) -> bool:
        """Удалить упражнение"""
        exercise = self.get_by_id(exercise_id)
        if exercise:
            self.db.delete(exercise)
            self.db.commit()
            return True
        return False
