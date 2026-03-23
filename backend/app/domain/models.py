"""
Domain Models (Доменные модели)
Это "сердце" приложения - чистые Python классы без зависимостей от фреймворков

Эти модели описывают ЧТО такое User, Lesson, Exercise в нашей предметной области,
но НЕ описывают КАК они хранятся в БД (это задача Infrastructure Layer)
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, field
from .enums import EnglishLevel, ExerciseType, DifficultyLevel, LessonStatus, UserRole


@dataclass
class User:
    """
    Пользователь платформы
    
    Атрибуты:
        id: Уникальный идентификатор
        email: Email для входа
        username: Имя пользователя
        hashed_password: Хешированный пароль
        level: Текущий уровень английского (A1-C1)
        total_xp: Общее количество опыта
        streak_days: Количество дней подряд занятий
        role: Роль пользователя (student/teacher/admin)
        created_at: Дата регистрации
        last_login: Последний вход
    """
    id: Optional[int] = None
    email: str = ""
    username: str = ""
    hashed_password: str = ""
    level: EnglishLevel = EnglishLevel.A1
    total_xp: int = 0
    streak_days: int = 0
    role: UserRole = UserRole.STUDENT
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    def can_access_lesson(self, lesson_level: EnglishLevel) -> bool:
        """
        Проверяет, может ли пользователь получить доступ к уроку
        
        Бизнес-правило: Можно проходить уроки своего уровня и на 1 уровень выше
        """
        user_level_index = list(EnglishLevel).index(self.level)
        lesson_level_index = list(EnglishLevel).index(lesson_level)
        
        return lesson_level_index <= user_level_index + 1
    
    def should_level_up(self) -> bool:
        """
        Проверяет, пора ли повысить уровень
        
        Бизнес-правило: Каждые 500 XP = новый уровень
        """
        xp_for_next_level = (list(EnglishLevel).index(self.level) + 1) * 500
        return self.total_xp >= xp_for_next_level


@dataclass
class Lesson:
    """
    Урок (набор упражнений на определённую тему)
    
    Атрибуты:
        id: Уникальный идентификатор
        title: Название урока (например, "Present Simple")
        description: Описание урока
        content: Теоретический материал урока
        level: Уровень (A1-C1)
        order: Порядковый номер в курсе
        xp_reward: Награда в XP за прохождение
        is_published: Опубликован ли урок
    """
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    content: Optional[str] = None
    level: EnglishLevel = EnglishLevel.A1
    order: int = 0
    xp_reward: int = 50
    is_published: bool = True
    created_at: Optional[datetime] = None


@dataclass
class Exercise:
    """
    Упражнение внутри урока
    
    Атрибуты:
        id: Уникальный идентификатор
        lesson_id: ID урока, к которому относится
        type: Тип упражнения (выбор, перевод, и т.д.)
        question: Текст вопроса
        correct_answer: Правильный ответ
        options: Варианты ответов (для multiple choice)
        difficulty: Сложность (1-3)
        xp_reward: Награда в XP
        explanation: Объяснение правильного ответа
    """
    id: Optional[int] = None
    lesson_id: Optional[int] = None
    type: ExerciseType = ExerciseType.MULTIPLE_CHOICE
    question: str = ""
    correct_answer: str = ""
    options: List[str] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    xp_reward: int = 10
    explanation: str = ""
    audio_url: Optional[str] = None  # Для аудирования
    
    def check_answer(self, user_answer: str) -> bool:
        """
        Проверяет правильность ответа
        
        Бизнес-правило: 
        - Для multiple choice - точное совпадение
        - Для type answer - case-insensitive сравнение
        - Для translation - допускается небольшая погрешность
        """
        if self.type == ExerciseType.MULTIPLE_CHOICE:
            return user_answer.strip() == self.correct_answer.strip()
        elif self.type == ExerciseType.TYPE_ANSWER:
            return user_answer.strip().lower() == self.correct_answer.strip().lower()
        elif self.type == ExerciseType.TRANSLATION:
            # Упрощённая проверка - в реальности нужен более сложный алгоритм
            return user_answer.strip().lower() == self.correct_answer.strip().lower()
        else:
            return user_answer.strip() == self.correct_answer.strip()


@dataclass
class UserProgress:
    """
    Прогресс пользователя по конкретному уроку
    
    Атрибуты:
        id: Уникальный идентификатор
        user_id: ID пользователя
        lesson_id: ID урока
        status: Статус прохождения
        xp_earned: Заработано XP в этом уроке
        exercises_completed: Количество завершённых упражнений
        exercises_total: Общее количество упражнений в уроке
        started_at: Когда начали урок
        completed_at: Когда завершили урок
    """
    id: Optional[int] = None
    user_id: Optional[int] = None
    lesson_id: Optional[int] = None
    status: LessonStatus = LessonStatus.NOT_STARTED
    xp_earned: int = 0
    exercises_completed: int = 0
    exercises_total: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def progress_percentage(self) -> float:
        """Вычисляет процент прохождения урока"""
        if self.exercises_total == 0:
            return 0.0
        return (self.exercises_completed / self.exercises_total) * 100


@dataclass
class ExerciseResult:
    """
    Результат выполнения одного упражнения
    
    Атрибуты:
        id: Уникальный идентификатор
        user_id: ID пользователя
        exercise_id: ID упражнения
        user_answer: Ответ пользователя
        is_correct: Правильный ли ответ
        xp_earned: Заработано XP
        completed_at: Когда выполнено
    """
    id: Optional[int] = None
    user_id: Optional[int] = None
    exercise_id: Optional[int] = None
    user_answer: str = ""
    is_correct: bool = False
    xp_earned: int = 0
    completed_at: Optional[datetime] = None


@dataclass
class Achievement:
    """
    Достижение (badge/trophy)
    
    Атрибуты:
        id: Уникальный идентификатор
        code: Уникальный код достижения
        name: Название
        description: Описание
        icon: Иконка (emoji или URL)
        xp_required: Требуемое количество XP (если применимо)
    """
    id: Optional[int] = None
    code: str = ""
    name: str = ""
    description: str = ""
    icon: str = "🏆"
    xp_required: Optional[int] = None


@dataclass
class UserAchievement:
    """
    Связь пользователя с достижением
    
    Атрибуты:
        id: Уникальный идентификатор
        user_id: ID пользователя
        achievement_id: ID достижения
        earned_at: Когда получено
    """
    id: Optional[int] = None
    user_id: Optional[int] = None
    achievement_id: Optional[int] = None
    earned_at: Optional[datetime] = None
