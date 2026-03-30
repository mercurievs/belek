"""
Domain Enums (Перечисления)
Эти enum'ы используются в доменных моделях
"""

from enum import Enum


class EnglishLevel(str, Enum):
    """Уровни английского языка по CEFR"""
    A1 = "A1"  # Beginner
    A2 = "A2"  # Elementary
    B1 = "B1"  # Intermediate
    B2 = "B2"  # Upper-Intermediate
    C1 = "C1"  # Advanced


class ExerciseType(str, Enum):
    """Типы упражнений"""
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"  # Выбор одного из вариантов
    TRANSLATION = "TRANSLATION"          # Перевод предложения
    TYPE_ANSWER = "TYPE_ANSWER"          # Ввод текста
    LISTENING = "LISTENING"              # Аудирование
    MATCH_PAIRS = "MATCH_PAIRS"          # Сопоставление пар


class DifficultyLevel(str, Enum):
    """Уровень сложности упражнения"""
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class LessonStatus(str, Enum):
    """Статус прохождения урока"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    LOCKED = "LOCKED"  # Урок заблокирован (не выполнены предыдущие)


class UserRole(str, Enum):
    """Роль пользователя в системе"""
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"


class Language(str, Enum):
    """Поддерживаемые языки обучения"""
    ENGLISH = "ENGLISH"
    KYRGYZ = "KYRGYZ"
