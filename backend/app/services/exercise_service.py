"""
Exercise Service
Бизнес-логика для работы с упражнениями
"""

from typing import Optional, List, Dict
from sqlalchemy.orm import Session

from app.infrastructure.repositories.exercise_repository import ExerciseRepository
from app.infrastructure.repositories.progress_repository import ProgressRepository
from app.infrastructure.repositories.user_repository import UserRepository
from app.domain.enums import ExerciseType


class ExerciseService:
    """
    Сервис для работы с упражнениями
    
    Содержит бизнес-логику для:
    - Получения упражнений
    - Проверки ответов
    - Начисления XP
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.exercise_repo = ExerciseRepository(db)
        self.progress_repo = ProgressRepository(db)
        self.user_repo = UserRepository(db)
    
    def get_all_exercises(self) -> List[Dict]:
        """
        Получить все упражнения для практики
        
        Returns:
            Список всех упражнений
        """
        exercises = self.exercise_repo.get_all()
        
        result = []
        for exercise in exercises:
            exercise_dict = {
                "id": exercise.id,
                "lesson_id": exercise.lesson_id,
                "type": exercise.type,
                "question": exercise.question,
                "difficulty": exercise.difficulty,
                "xp_reward": exercise.xp_reward,
                "explanation": exercise.explanation
            }
            
            # Добавляем варианты ответов для multiple choice
            if exercise.type == ExerciseType.MULTIPLE_CHOICE:
                options = self.exercise_repo.get_options(exercise)
                exercise_dict["options"] = options
            
            # Добавляем аудио URL если есть
            if exercise.audio_url:
                exercise_dict["audio_url"] = exercise.audio_url
            
            result.append(exercise_dict)
        
        return result
    
    def get_exercise_by_id(self, exercise_id: int) -> Optional[Dict]:
        """
        Получить упражнение по ID
        
        Args:
            exercise_id: ID упражнения
        
        Returns:
            Упражнение или None
        """
        exercise = self.exercise_repo.get_by_id(exercise_id)
        if not exercise:
            return None
        
        exercise_dict = {
            "id": exercise.id,
            "lesson_id": exercise.lesson_id,
            "type": exercise.type,
            "question": exercise.question,
            "difficulty": exercise.difficulty,
            "xp_reward": exercise.xp_reward,
            "explanation": exercise.explanation
        }
        
        # Добавляем варианты ответов для multiple choice
        if exercise.type == ExerciseType.MULTIPLE_CHOICE:
            options = self.exercise_repo.get_options(exercise)
            exercise_dict["options"] = options
        
        # Добавляем аудио URL если есть
        if exercise.audio_url:
            exercise_dict["audio_url"] = exercise.audio_url
        
        return exercise_dict
    
    def get_lesson_exercises(self, lesson_id: int) -> List[Dict]:
        """
        Получить все упражнения урока
        
        Args:
            lesson_id: ID урока
        
        Returns:
            Список упражнений
        """
        exercises = self.exercise_repo.get_by_lesson_id(lesson_id)
        
        result = []
        for exercise in exercises:
            exercise_dict = {
                "id": exercise.id,
                "type": exercise.type,
                "question": exercise.question,
                "difficulty": exercise.difficulty,
                "xp_reward": exercise.xp_reward,
                "explanation": exercise.explanation
            }
            
            # Добавляем варианты ответов для multiple choice
            if exercise.type == ExerciseType.MULTIPLE_CHOICE:
                options = self.exercise_repo.get_options(exercise)
                exercise_dict["options"] = options
            
            # Добавляем аудио URL если есть
            if exercise.audio_url:
                exercise_dict["audio_url"] = exercise.audio_url
            
            result.append(exercise_dict)
        
        return result
    
    def submit_answer(
        self, 
        user_id: int, 
        exercise_id: int, 
        lesson_id: int,
        user_answer: str
    ) -> Dict:
        """
        Проверяет ответ пользователя на упражнение
        
        Args:
            user_id: ID пользователя
            exercise_id: ID упражнения
            lesson_id: ID урока
            user_answer: Ответ пользователя
        
        Returns:
            Словарь с результатом проверки
        
        Бизнес-логика:
        1. Проверить правильность ответа
        2. Начислить XP если правильно
        3. Сохранить результат
        4. Обновить прогресс урока
        5. Проверить, не нужно ли повысить уровень пользователя
        """
        # Получаем упражнение
        exercise = self.exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise ValueError("Упражнение не найдено")
        
        # Проверяем ответ
        is_correct = self._check_answer(exercise, user_answer)
        
        # Начисляем XP только за правильный ответ
        xp_earned = exercise.xp_reward if is_correct else 0
        
        # Сохраняем результат упражнения
        self.progress_repo.save_exercise_result(
            user_id=user_id,
            exercise_id=exercise_id,
            user_answer=user_answer,
            is_correct=is_correct,
            xp_earned=xp_earned
        )
        
        # Обновляем прогресс урока
        progress = self.progress_repo.complete_exercise(
            user_id=user_id,
            lesson_id=lesson_id,
            xp_earned=xp_earned
        )
        
        # Обновляем общий XP пользователя
        user = self.user_repo.update_xp(user_id, xp_earned)
        
        return {
            "is_correct": is_correct,
            "correct_answer": exercise.correct_answer if not is_correct else None,
            "explanation": exercise.explanation if not is_correct else None,
            "xp_earned": xp_earned,
            "new_total_xp": user.total_xp if user else 0,
            "progress": {
                "exercises_completed": progress.exercises_completed,
                "exercises_total": progress.exercises_total,
                "lesson_completed": progress.exercises_completed >= progress.exercises_total
            }
        }
    
    def _check_answer(self, exercise, user_answer: str) -> bool:
        """
        Внутренний метод для проверки ответа
        
        Разная логика для разных типов упражнений
        """
        correct_answer = exercise.correct_answer.strip()
        user_answer = user_answer.strip()
        
        if exercise.type == ExerciseType.MULTIPLE_CHOICE:
            # Точное совпадение для выбора варианта
            return user_answer == correct_answer
        
        elif exercise.type == ExerciseType.TYPE_ANSWER:
            # Case-insensitive для ввода текста
            return user_answer.lower() == correct_answer.lower()
        
        elif exercise.type == ExerciseType.TRANSLATION:
            # Для перевода - упрощённая проверка
            # В продакшене можно использовать более сложные алгоритмы (Levenshtein distance)
            return user_answer.lower() == correct_answer.lower()
        
        else:
            # По умолчанию - точное совпадение
            return user_answer == correct_answer
