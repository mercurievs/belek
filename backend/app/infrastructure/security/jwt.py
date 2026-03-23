"""
JWT Token Management
Создание и валидация JWT токенов для аутентификации
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Создаёт JWT access token
    
    Args:
        data: Данные для включения в токен (обычно {"sub": user_id})
        expires_delta: Время жизни токена (по умолчанию из настроек)
    
    Returns:
        JWT токен в виде строки
    
    Example:
        token = create_access_token({"sub": "user@example.com"})
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Декодирует и валидирует JWT токен
    
    Args:
        token: JWT токен
    
    Returns:
        Словарь с данными из токена или None если токен невалиден
    
    Example:
        payload = decode_access_token(token)
        if payload:
            user_email = payload.get("sub")
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
