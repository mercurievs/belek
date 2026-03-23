"""Инициализация PostgreSQL - создание БД и таблиц"""
import sys
from sqlalchemy import create_engine, text

# Hardcoded URL
ADMIN_URL = "postgresql://postgres:42429364@localhost:5432/postgres"
DB_URL = "postgresql://postgres:42429364@localhost:5432/english_learning"

print("🔧 Инициализация PostgreSQL...")

try:
    # Создаем БД если не существует
    print("1. Подключаюсь к PostgreSQL...")
    admin_engine = create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")
    
    with admin_engine.connect() as conn:
        print("2. Проверяю существование БД...")
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='english_learning'"))
        
        if not result.scalar():
            print("3. Создаю базу данных english_learning...")
            conn.execute(text("CREATE DATABASE english_learning"))
            print("   ✅ База данных создана!")
        else:
            print("   ✅ База данных уже существует")
    
    admin_engine.dispose()
    
    # Создаем таблицы
    print("4. Создаю таблицы...")
    db_engine = create_engine(DB_URL)
    
    # Импортируем Base и модели
    sys.path.insert(0, '.')
    from app.infrastructure.database.base import Base
    import app.infrastructure.database.models  # Это загрузит все модели
    
    Base.metadata.create_all(bind=db_engine)
    print("   ✅ Таблицы созданы!")
    
    db_engine.dispose()
    
    print("\n" + "="*50)
    print("🎉 PostgreSQL успешно настроен!")
    print("="*50)
    print(f"📍 URL: {DB_URL}")
    print("\n📝 Следующий шаг:")
    print("   python seed_comprehensive_full.py")
    print("   или")  
    print("   python create_admin.py")
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    print("\n🔍 Возможные причины:")
    print("  1. PostgreSQL не запущен")
    print("  2. Неверный пароль (текущий: 42429364)")
    print("  3. PostgreSQL использует другой порт (не 5432)")
    print("  4. Настройки pg_hba.conf требуют другой метод аутентификации")
    sys.exit(1)
