"""
Константы приложения
Все "магические числа" и строки должны быть здесь
"""

# XP (Experience Points) система
XP_PER_CORRECT_ANSWER = 10
XP_PER_LESSON_COMPLETION = 50
XP_FOR_PERFECT_LESSON = 100  # Если все ответы правильные

# Уровни английского языка (CEFR)
ENGLISH_LEVELS = ["A1", "A2", "B1", "B2", "C1"]

# Типы упражнений
EXERCISE_TYPES = {
    "MULTIPLE_CHOICE": "multiple_choice",  # Выбор одного ответа
    "TRANSLATION": "translation",          # Перевод
    "TYPE_ANSWER": "type_answer",          # Ввод текста
    "LISTENING": "listening",              # Аудирование
    "MATCH_PAIRS": "match_pairs",          # Сопоставление пар
}

# Сложность упражнений
DIFFICULTY_LEVELS = {
    "EASY": 1,
    "MEDIUM": 2,
    "HARD": 3,
}

# Прогресс урока
LESSON_STATUS = {
    "NOT_STARTED": "not_started",
    "IN_PROGRESS": "in_progress",
    "COMPLETED": "completed",
}

# Streak (серия занятий)
STREAK_THRESHOLD_HOURS = 24  # Если не занимались 24 часа, streak сбрасывается

# Достижения (Achievements)
ACHIEVEMENTS = {
    "FIRST_LESSON": {
        "name": "Первые шаги",
        "description": "Пройдено первое упражнение",
        "icon": "🎯",
    },
    "WEEK_STREAK": {
        "name": "Неделя подряд",
        "description": "Занимались 7 дней подряд",
        "icon": "🔥",
    },
    "HUNDRED_XP": {
        "name": "Сотня!",
        "description": "Заработано 100 XP",
        "icon": "⭐",
    },
    "LEVEL_UP": {
        "name": "Повышение уровня",
        "description": "Достигнут новый уровень",
        "icon": "🚀",
    },
}

# Валидация
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 100
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 50
