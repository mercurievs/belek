"""
Production seed script.
Создает полный английский и кыргызский контент переносимым способом
для SQLite и PostgreSQL.
"""

from app.infrastructure.database.base import Base, engine
from seed_full_db import seed_database
from seed_kyrgyz_a2 import seed_kyrgyz_a2


def seed_all() -> None:
    Base.metadata.create_all(bind=engine)
    seed_database()
    seed_kyrgyz_a2()


if __name__ == "__main__":
    seed_all()