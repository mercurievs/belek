"""
Создание админа
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.infrastructure.database.base import SessionLocal
from app.infrastructure.database.models import UserModel
from app.domain.enums import UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db = SessionLocal()
    try:
        # Проверяем есть ли уже админ
        admin = db.query(UserModel).filter(UserModel.email == "admin@admin.com").first()
        if admin:
            print("❌ Админ уже существует")
            print(f"Email: admin@admin.com")
            return
        
        # Создаём админа
        hashed_password = pwd_context.hash("admin123")
        admin = UserModel(
            email="admin@admin.com",
            username="Admin",
            hashed_password=hashed_password,
            role=UserRole.ADMIN.value,
            level="A1",
            total_xp=0,
            streak_days=0,
            is_active=True
        )
        db.add(admin)
        db.commit()
        
        print("✅ Админ успешно создан!")
        print("Email: admin@admin.com")
        print("Password: admin123")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
