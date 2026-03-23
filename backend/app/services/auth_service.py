"""
Authentication Service
Бизнес-логика для авторизации и аутентификации
"""

from typing import Optional
from sqlalchemy.orm import Session
from datetime import timedelta

from app.infrastructure.repositories.user_repository import UserRepository
from app.infrastructure.security.password import verify_password, get_password_hash
from app.infrastructure.security.jwt import create_access_token
from app.core.config import settings
from app.domain.enums import EnglishLevel, UserRole


class AuthService:
    """
    Сервис авторизации
    
    Содержит бизнес-логику для:
    - Регистрации пользователей
    - Аутентификации (логин)
    - Валидации токенов
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register_user(
        self, 
        email: str, 
        username: str, 
        password: str
    ) -> dict:
        """
        Регистрирует нового пользователя
        
        Args:
            email: Email пользователя
            username: Имя пользователя
            password: Пароль в открытом виде
        
        Returns:
            Словарь с данными пользователя и токеном
        
        Raises:
            ValueError: Если email или username уже заняты
        """
        # Проверяем, существует ли email
        existing_user = self.user_repo.get_by_email(email)
        if existing_user:
            raise ValueError("Email уже зарегистрирован")
        
        # Проверяем, существует ли username
        existing_username = self.user_repo.get_by_username(username)
        if existing_username:
            raise ValueError("Имя пользователя уже занято")
        
        # Хешируем пароль
        hashed_password = get_password_hash(password)
        
        # Создаём пользователя
        user = self.user_repo.create(
            email=email,
            username=username,
            hashed_password=hashed_password
        )
        
        # Создаём JWT токен
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "level": user.level,
                "total_xp": user.total_xp,
                "streak_days": user.streak_days
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """
        Аутентифицирует пользователя (логин)
        
        Args:
            email: Email пользователя
            password: Пароль в открытом виде
        
        Returns:
            Словарь с данными пользователя и токеном, или None если неверные данные
        """
        # Получаем пользователя из БД
        user = self.user_repo.get_by_email(email)
        
        # Проверяем существование и активность
        if not user or not user.is_active:
            return None
        
        # Проверяем пароль
        if not verify_password(password, user.hashed_password):
            return None
        
        # Обновляем время последнего входа
        self.user_repo.update_last_login(user.id)
        
        # Создаём JWT токен
        access_token = create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "level": user.level,
                "total_xp": user.total_xp,
                "streak_days": user.streak_days
            },
            "access_token": access_token,
            "token_type": "bearer"
        }
    
    def get_current_user(self, email: str) -> Optional[dict]:
        """
        Получает текущего пользователя по email из токена
        
        Args:
            email: Email из JWT токена
        
        Returns:
            Словарь с данными пользователя или None
        """
        user = self.user_repo.get_by_email(email)
        
        if not user or not user.is_active:
            return None
        
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "level": user.level,
            "total_xp": user.total_xp,
            "streak_days": user.streak_days,
            "role": user.role
        }
