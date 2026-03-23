"""
Password Hashing and Verification
Безопасное хеширование паролей с использованием bcrypt
"""

from passlib.context import CryptContext

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет, соответствует ли введённый пароль хешированному
    
    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хешированный пароль из БД
    
    Returns:
        True если пароли совпадают, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Хеширует пароль для безопасного хранения в БД
    
    Args:
        password: Пароль в открытом виде
    
    Returns:
        Хешированный пароль
    """
    return pwd_context.hash(password)
