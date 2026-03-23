"""
User Repository
Паттерн Repository для работы с пользователями в БД
Отделяет бизнес-логику от деталей работы с БД
"""

from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime

from app.infrastructure.database.models import UserModel
from app.domain.enums import EnglishLevel, UserRole


class UserRepository:
    """
    Репозиторий для работы с пользователями
    
    Предоставляет методы для CRUD операций с пользователями
    без привязки к конкретным деталям реализации БД
    """
    
    def __init__(self, db: Session):
        """
        Args:
            db: Сессия SQLAlchemy
        """
        self.db = db
    
    def create(self, email: str, username: str, hashed_password: str) -> UserModel:
        """
        Создаёт нового пользователя
        
        Args:
            email: Email пользователя
            username: Имя пользователя
            hashed_password: Хешированный пароль
        
        Returns:
            Созданная модель пользователя
        """
        db_user = UserModel(
            email=email,
            username=username,
            hashed_password=hashed_password,
            level=EnglishLevel.A1,
            total_xp=0,
            streak_days=0,
            role=UserRole.STUDENT,
            is_active=True
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """Получить пользователя по ID"""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[UserModel]:
        """Получить пользователя по email"""
        return self.db.query(UserModel).filter(UserModel.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Получить пользователя по username"""
        return self.db.query(UserModel).filter(UserModel.username == username).first()
    
    def update_xp(self, user_id: int, xp_to_add: int) -> Optional[UserModel]:
        """
        Добавляет XP пользователю
        
        Args:
            user_id: ID пользователя
            xp_to_add: Сколько XP добавить
        
        Returns:
            Обновлённая модель пользователя
        """
        user = self.get_by_id(user_id)
        if user:
            user.total_xp += xp_to_add
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def update_level(self, user_id: int, new_level: EnglishLevel) -> Optional[UserModel]:
        """Обновляет уровень английского пользователя"""
        user = self.get_by_id(user_id)
        if user:
            user.level = new_level
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def update_streak(self, user_id: int, streak_days: int) -> Optional[UserModel]:
        """Обновляет streak (серию занятий) пользователя"""
        user = self.get_by_id(user_id)
        if user:
            user.streak_days = streak_days
            user.last_activity = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def update_last_login(self, user_id: int) -> Optional[UserModel]:
        """Обновляет время последнего входа"""
        user = self.get_by_id(user_id)
        if user:
            user.last_login = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """
        Получить список пользователей с пагинацией
        
        Args:
            skip: Сколько записей пропустить
            limit: Максимальное количество записей
        
        Returns:
            Список пользователей
        """
        return self.db.query(UserModel).offset(skip).limit(limit).all()
    
    def delete(self, user_id: int) -> bool:
        """
        Удалить пользователя
        
        Args:
            user_id: ID пользователя
        
        Returns:
            True если удалён, False если не найден
        """
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
