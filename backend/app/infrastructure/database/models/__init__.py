"""
ORM Models - SQLAlchemy модели для базы данных
Это Infrastructure Layer - описывает КАК данные хранятся в БД
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from app.infrastructure.database.base import Base
from app.domain.enums import EnglishLevel, ExerciseType, DifficultyLevel, LessonStatus, UserRole


class UserModel(Base):
    """
    ORM модель пользователя
    Таблица: users
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Прогресс и уровень
    level = Column(Enum(EnglishLevel), default=EnglishLevel.A1, nullable=False)
    total_xp = Column(Integer, default=0, nullable=False)
    streak_days = Column(Integer, default=0, nullable=False)
    
    # Роль и статус
    role = Column(Enum(UserRole), default=UserRole.STUDENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships (связи с другими таблицами)
    progress = relationship("UserProgressModel", back_populates="user", cascade="all, delete-orphan")
    exercise_results = relationship("ExerciseResultModel", back_populates="user", cascade="all, delete-orphan")
    achievements = relationship("UserAchievementModel", back_populates="user", cascade="all, delete-orphan")


class LessonModel(Base):
    """
    ORM модель урока
    Таблица: lessons
    """
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    content = Column(Text, nullable=True)  # Теоретический материал урока
    
    # Характеристики урока
    level = Column(Enum(EnglishLevel), nullable=False, index=True)
    order = Column(Integer, nullable=False)  # Порядок в курсе
    xp_reward = Column(Integer, default=50, nullable=False)
    
    # Статус
    is_published = Column(Boolean, default=True, nullable=False)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    exercises = relationship("ExerciseModel", back_populates="lesson", cascade="all, delete-orphan")
    user_progress = relationship("UserProgressModel", back_populates="lesson", cascade="all, delete-orphan")


class ExerciseModel(Base):
    """
    ORM модель упражнения
    Таблица: exercises
    """
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    
    # Тип и сложность
    type = Column(Enum(ExerciseType), nullable=False)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.MEDIUM)
    
    # Контент упражнения
    question = Column(Text, nullable=False)
    correct_answer = Column(String(500), nullable=False)
    options = Column(Text, nullable=True)  # JSON строка с вариантами ответов
    explanation = Column(Text, nullable=True)  # Объяснение правильного ответа
    
    # Медиа
    audio_url = Column(String(500), nullable=True)  # URL аудиофайла для listening
    image_url = Column(String(500), nullable=True)  # URL изображения
    
    # Награда
    xp_reward = Column(Integer, default=10, nullable=False)
    
    # Порядок в уроке
    order = Column(Integer, nullable=False)
    
    # Временные метки
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    lesson = relationship("LessonModel", back_populates="exercises")
    results = relationship("ExerciseResultModel", back_populates="exercise", cascade="all, delete-orphan")


class UserProgressModel(Base):
    """
    ORM модель прогресса пользователя по уроку
    Таблица: user_progress
    """
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    
    # Статус и прогресс
    status = Column(Enum(LessonStatus), default=LessonStatus.NOT_STARTED, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)
    exercises_completed = Column(Integer, default=0, nullable=False)
    exercises_total = Column(Integer, default=0, nullable=False)
    
    # Временные метки
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("UserModel", back_populates="progress")
    lesson = relationship("LessonModel", back_populates="user_progress")


class ExerciseResultModel(Base):
    """
    ORM модель результата выполнения упражнения
    Таблица: exercise_results
    """
    __tablename__ = "exercise_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    
    # Результат
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    xp_earned = Column(Integer, default=0, nullable=False)
    
    # Временная метка
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="exercise_results")
    exercise = relationship("ExerciseModel", back_populates="results")


class AchievementModel(Base):
    """
    ORM модель достижения
    Таблица: achievements
    """
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(100), default="🏆")
    xp_required = Column(Integer, nullable=True)
    
    # Временная метка
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user_achievements = relationship("UserAchievementModel", back_populates="achievement", cascade="all, delete-orphan")


class UserAchievementModel(Base):
    """
    ORM модель связи пользователя с достижением
    Таблица: user_achievements
    """
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id", ondelete="CASCADE"), nullable=False)
    
    # Временная метка
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("UserModel", back_populates="achievements")
    achievement = relationship("AchievementModel", back_populates="user_achievements")
