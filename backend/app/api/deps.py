"""
API Dependencies
Зависимости для FastAPI endpoints (аутентификация, получение БД и т.д.)
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.infrastructure.database.base import get_db
from app.infrastructure.security.jwt import decode_access_token
from app.services.auth_service import AuthService

# OAuth2 схема для получения токена из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> dict:
    """
    Dependency для получения текущего аутентифицированного пользователя
    
    Использование в endpoints:
        @router.get("/profile")
        def get_profile(current_user: dict = Depends(get_current_user)):
            return current_user
    
    Args:
        token: JWT токен из заголовка Authorization
        db: Сессия базы данных
    
    Returns:
        Словарь с данными пользователя
    
    Raises:
        HTTPException: Если токен невалиден или пользователь не найден
    """
    # Декодируем токен
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Получаем email из токена
    email: Optional[str] = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидный токен аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Получаем пользователя из БД
    auth_service = AuthService(db)
    user = auth_service.get_current_user(email)
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_active_user(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """
    Dependency для получения активного пользователя
    (для будущего функционала деактивации аккаунтов)
    """
    return current_user
