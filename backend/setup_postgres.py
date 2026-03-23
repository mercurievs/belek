"""
Скрипт настройки PostgreSQL базы данных
Создает базу данных и таблицы
"""
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from app.infrastructure.database.base import Base
from app.infrastructure.database.models import *  # Импорт всех моделей

def create_database():
    """Создает базу данных если её нет"""
    # Подключаемся к postgres БД для создания нашей БД
    print("Введите пароль для пользователя postgres:")
    password = input().strip()
    
    admin_url = f"postgresql://postgres:{password}@localhost:5432/postgres"
    
    try:
        engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
        with engine.connect() as conn:
            # Проверяем существует ли БД
            result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='english_learning'"))
            exists = result.scalar() is not None
            
            if not exists:
                print("Создаю базу данных english_learning...")
                conn.execute(text("CREATE DATABASE english_learning"))
                print("✅ База данных создана!")
            else:
                print("✅ База данных уже существует")
        
        # Обновляем DATABASE_URL в config.py
        config_path = "app/core/config.py"
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        
        # Заменяем строку подключения
        new_url = f"postgresql://postgres:{password}@localhost:5432/english_learning"
        if 'DATABASE_URL: str = "postgresql://' in content:
            import re
            content = re.sub(
                r'DATABASE_URL: str = "postgresql://[^"]*"',
                f'DATABASE_URL: str = "{new_url}"',
                content
            )
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Конфигурация обновлена")
        
        # Создаем таблицы
        print("\nСоздаю таблицы...")
        db_engine = create_engine(new_url)
        Base.metadata.create_all(bind=db_engine)
        print("✅ Таблицы созданы!")
        
        print("\n🎉 PostgreSQL настроен успешно!")
        print(f"📍 URL базы данных: {new_url}")
        print("\n⚠️  Теперь нужно заполнить базу данных уроками и упражнениями")
        print("   Запустите: python seed_comprehensive_full.py")
        
    except OperationalError as e:
        print(f"❌ Ошибка подключения: {e}")
        print("Проверьте, что PostgreSQL запущен и пароль правильный")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_database()
