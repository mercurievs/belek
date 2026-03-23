from sqlalchemy import create_engine, text

DB_URL = "postgresql://postgres:42429364@localhost:5432/english_learning"
ADMIN_URL = "postgresql://postgres:42429364@localhost:5432/postgres"

try:
    print("Создаю БД...")
    engine = create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 FROM pg_database WHERE datname='english_learning'"))
        if not result.scalar():
            conn.execute(text("CREATE DATABASE english_learning"))
            print("OK: БД создана!")
        else:
            print("OK: БД существует!")
    engine.dispose()
    print("SUCCESS")
except Exception as e:
    print(f"ERROR: {e}")
