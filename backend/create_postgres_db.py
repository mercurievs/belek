"""
Простой скрипт создания PostgreSQL базы данных и таблиц
"""
from sqlalchemy import create_engine, text
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import *

# URL с вашим паролем
DB_URL = "postgresql://postgres:42429364@localhost:5432/english_learning"

print("Создаю базу данных и таблицы...")

try:
    # Пытаемся создать БД (если не существует)
    admin_url = "postgresql://postgres:42429364@localhost:5432/postgres"
    engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='english_learning'"))
        if not result.scalar():
            conn.execute(text("CREATE DATABASE english_learning"))
            print("✅ База данных создана!")
        else:
            print("✅ База данных уже существует")
    
    # Создаем таблицы
    db_engine = create_engine(DB_URL)
    Base.metadata.create_all(bind=db_engine)
    print("✅ Таблицы созданы!")
    
    print("\n🎉 PostgreSQL готов к работе!")
    print("\n⚠️  Теперь заполните базу данных:")
    print("   python seed_comprehensive_full.py")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    print("\nПроверьте:")
    print("1. PostgreSQL запущен")
    print("2. Пароль правильный (42429364)")
    print("3. Порт 5432 доступен")
