"""
Pydantic Schemas for Users
Схемы для валидации запросов и ответов API
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

from app.domain.enums import EnglishLevel, UserRole


class UserRegister(BaseModel):
    """Схема для регистрации пользователя"""
    email: EmailStr = Field(..., description="Email пользователя")
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    password: str = Field(..., min_length=8, max_length=100, description="Пароль")


class UserLogin(BaseModel):
    """Схема для входа пользователя"""
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., description="Пароль")


class UserResponse(BaseModel):
    """Схема ответа с данными пользователя"""
    id: int
    email: str
    username: str
    level: EnglishLevel
    total_xp: int
    streak_days: int
    role: Optional[UserRole] = UserRole.STUDENT
    
    class Config:
        from_attributes = True  # Для совместимости с ORM моделями


class TokenResponse(BaseModel):
    """Схема ответа с токеном"""
    access_token: str
    token_type: str = "bearer"


class AuthResponse(BaseModel):
    """Схема ответа при регистрации/входе"""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"
