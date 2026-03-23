"""
Authentication Endpoints
API endpoints для регистрации и входа
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.base import get_db
from app.services.auth_service import AuthService
from app.api.v1.schemas.user import UserRegister, UserLogin, AuthResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Регистрация нового пользователя
    
    - **email**: Email пользователя (уникальный)
    - **username**: Имя пользователя (уникальное, 3-50 символов)
    - **password**: Пароль (минимум 8 символов)
    
    Returns:
        - Данные пользователя
        - JWT токен для дальнейшей аутентификации
    """
    auth_service = AuthService(db)
    
    try:
        result = auth_service.register_user(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=AuthResponse)
def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Вход в систему (аутентификация)
    
    - **email**: Email пользователя
    - **password**: Пароль
    
    Returns:
        - Данные пользователя
        - JWT токен для дальнейшей аутентификации
    """
    auth_service = AuthService(db)
    
    result = auth_service.authenticate_user(
        email=user_data.email,
        password=user_data.password
    )
    
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return result


@router.get("/me", response_model=dict)
def get_current_user_profile(
    current_user: dict = Depends(get_current_user)
):
    """
    Получить профиль текущего пользователя
    
    Требуется аутентификация (JWT токен в заголовке)
    """
    return current_user
