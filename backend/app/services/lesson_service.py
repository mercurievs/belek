"""
Lesson Service
Бизнес-логика для работы с уроками
"""

from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from app.infrastructure.repositories.lesson_repository import LessonRepository
from app.infrastructure.repositories.exercise_repository import ExerciseRepository
from app.infrastructure.repositories.progress_repository import ProgressRepository
from app.domain.enums import EnglishLevel, LessonStatus, Language


class LessonService:
    """
    Сервис для работы с уроками
    
    Содержит бизнес-логику для:
    - Получения списка уроков
    - Получения деталей урока
    - Проверки доступа к уроку
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.lesson_repo = LessonRepository(db)
        self.exercise_repo = ExerciseRepository(db)
        self.progress_repo = ProgressRepository(db)
    
    def get_all_lessons(
        self, 
        user_id: Optional[int] = None,
        level: Optional[EnglishLevel] = None,
        language: Language = Language.ENGLISH
    ) -> List[Dict]:
        """
        Получить список всех уроков с прогрессом пользователя
        
        Args:
            user_id: ID пользователя (опционально)
            level: Фильтр по уровню (опционально)
            language: Язык обучения
        
        Returns:
            Список уроков с информацией о прогрессе
        """
        # Получаем уроки
        if level:
            lessons = self.lesson_repo.get_by_level(level, language)
        else:
            lessons = self.lesson_repo.get_all_published(language=language)
        
        # Если пользователь указан, добавляем прогресс
        if user_id:
            user_progress = self.progress_repo.get_user_progress(user_id)
            progress_map = {p.lesson_id: p for p in user_progress}
        else:
            progress_map = {}
        
        result = []
        for lesson in lessons:
            lesson_dict = {
                "id": lesson.id,
                "title": lesson.title,
                "description": lesson.description,
                "level": lesson.level,
                "language": lesson.language,
                "order": lesson.order,
                "xp_reward": lesson.xp_reward
            }
            
            # Добавляем прогресс если есть
            if lesson.id in progress_map:
                progress = progress_map[lesson.id]
                lesson_dict["progress"] = {
                    "status": progress.status,
                    "exercises_completed": progress.exercises_completed,
                    "exercises_total": progress.exercises_total,
                    "xp_earned": progress.xp_earned
                }
            else:
                lesson_dict["progress"] = {
                    "status": LessonStatus.NOT_STARTED,
                    "exercises_completed": 0,
                    "exercises_total": 0,
                    "xp_earned": 0
                }
            
            result.append(lesson_dict)
        
        return result
    
    def get_lesson_details(self, lesson_id: int, user_id: Optional[int] = None) -> Optional[Dict]:
        """
        Получить детали конкретного урока
        
        Args:
            lesson_id: ID урока
            user_id: ID пользователя (опционально)
        
        Returns:
            Словарь с деталями урока
        """
        lesson = self.lesson_repo.get_by_id(lesson_id)
        if not lesson:
            return None
        
        # Получаем упражнения урока
        exercises = self.exercise_repo.get_by_lesson_id(lesson_id)
        
        lesson_dict = {
            "id": lesson.id,
            "title": lesson.title,
            "description": lesson.description,
            "level": lesson.level,
            "order": lesson.order,
            "xp_reward": lesson.xp_reward,
            "exercises_count": len(exercises)
        }
        
        # Добавляем прогресс если указан пользователь
        if user_id:
            progress = self.progress_repo.get_or_create_progress(
                user_id=user_id,
                lesson_id=lesson_id,
                exercises_total=len(exercises)
            )
            
            lesson_dict["progress"] = {
                "status": progress.status,
                "exercises_completed": progress.exercises_completed,
                "exercises_total": progress.exercises_total,
                "xp_earned": progress.xp_earned
            }
        
        return lesson_dict
    
    def start_lesson(self, user_id: int, lesson_id: int) -> Dict:
        """
        Начать урок (изменить статус на IN_PROGRESS)
        
        Args:
            user_id: ID пользователя
            lesson_id: ID урока
        
        Returns:
            Обновлённый прогресс
        """
        lesson = self.lesson_repo.get_by_id(lesson_id)
        if not lesson:
            raise ValueError("Урок не найден")
        
        # Получаем количество упражнений
        exercises = self.exercise_repo.get_by_lesson_id(lesson_id)
        
        # Создаём или обновляем прогресс
        progress = self.progress_repo.get_or_create_progress(
            user_id=user_id,
            lesson_id=lesson_id,
            exercises_total=len(exercises)
        )
        
        # Начинаем урок
        progress = self.progress_repo.start_lesson(user_id, lesson_id)
        
        return {
            "lesson_id": lesson_id,
            "status": progress.status,
            "exercises_total": progress.exercises_total
        }
