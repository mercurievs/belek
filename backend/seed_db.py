"""
Seed Database Script
Заполняет базу данных тестовыми данными
"""

from sqlalchemy.orm import Session
from app.infrastructure.database.base import SessionLocal, engine, Base
from app.infrastructure.database.models import (
    UserModel, LessonModel, ExerciseModel, AchievementModel
)
from app.domain.enums import EnglishLevel, ExerciseType, DifficultyLevel
from app.infrastructure.security.password import get_password_hash
import json


def seed_database():
    """Заполняет БД тестовыми данными"""
    
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("🌱 Начинаем заполнение базы данных...")
        
        # 1. Создаём тестового пользователя
        print("\n👤 Создаём пользователей...")
        test_user = UserModel(
            email="test@example.com",
            username="testuser",
            hashed_password=get_password_hash("password123"[:72]),  # Ограничиваем длину для bcrypt
            level=EnglishLevel.A1,
            total_xp=0,
            streak_days=0
        )
        db.add(test_user)
        db.commit()
        print("✅ Создан пользователь: test@example.com / password123")
        
        # 2. Создаём уроки для уровня A1
        print("\n📚 Создаём уроки...")
        
        # Урок 1: Present Simple
        lesson1 = LessonModel(
            title="Present Simple - Настоящее простое время",
            description="Изучаем базовую грамматику английского языка: Present Simple",
            level=EnglishLevel.A1,
            order=1,
            xp_reward=50
        )
        db.add(lesson1)
        db.commit()
        db.refresh(lesson1)
        print(f"✅ Создан урок: {lesson1.title}")
        
        # Упражнения для урока 1
        exercises_lesson1 = [
            {
                "type": ExerciseType.MULTIPLE_CHOICE,
                "question": "I ___ to school every day.",
                "correct_answer": "go",
                "options": ["go", "goes", "going", "went"],
                "difficulty": DifficultyLevel.EASY,
                "explanation": "С местоимением 'I' используется форма глагола без окончания -s",
                "order": 1
            },
            {
                "type": ExerciseType.MULTIPLE_CHOICE,
                "question": "She ___ English very well.",
                "correct_answer": "speaks",
                "options": ["speak", "speaks", "speaking", "spoke"],
                "difficulty": DifficultyLevel.EASY,
                "explanation": "С местоимениями he/she/it в Present Simple глагол получает окончание -s",
                "order": 2
            },
            {
                "type": ExerciseType.TYPE_ANSWER,
                "question": "Переведите: Я люблю английский язык",
                "correct_answer": "I love English",
                "options": None,
                "difficulty": DifficultyLevel.MEDIUM,
                "explanation": "I love English - правильный перевод",
                "order": 3
            }
        ]
        
        for ex_data in exercises_lesson1:
            exercise = ExerciseModel(
                lesson_id=lesson1.id,
                type=ex_data["type"],
                question=ex_data["question"],
                correct_answer=ex_data["correct_answer"],
                options=json.dumps(ex_data["options"]) if ex_data["options"] else None,
                difficulty=ex_data["difficulty"],
                explanation=ex_data["explanation"],
                xp_reward=10,
                order=ex_data["order"]
            )
            db.add(exercise)
        
        db.commit()
        print(f"✅ Создано {len(exercises_lesson1)} упражнений для урока 1")
        
        # Урок 2: Pronouns
        lesson2 = LessonModel(
            title="Personal Pronouns - Личные местоимения",
            description="Изучаем личные местоимения в английском языке",
            level=EnglishLevel.A1,
            order=2,
            xp_reward=50
        )
        db.add(lesson2)
        db.commit()
        db.refresh(lesson2)
        print(f"✅ Создан урок: {lesson2.title}")
        
        # Упражнения для урока 2
        exercises_lesson2 = [
            {
                "type": ExerciseType.MULTIPLE_CHOICE,
                "question": "___ am a student.",
                "correct_answer": "I",
                "options": ["I", "You", "He", "She"],
                "difficulty": DifficultyLevel.EASY,
                "explanation": "I (я) - местоимение первого лица единственного числа",
                "order": 1
            },
            {
                "type": ExerciseType.MULTIPLE_CHOICE,
                "question": "___ is my friend.",
                "correct_answer": "He",
                "options": ["I", "You", "He", "They"],
                "difficulty": DifficultyLevel.EASY,
                "explanation": "He (он) используется для обозначения мужчины",
                "order": 2
            }
        ]
        
        for ex_data in exercises_lesson2:
            exercise = ExerciseModel(
                lesson_id=lesson2.id,
                type=ex_data["type"],
                question=ex_data["question"],
                correct_answer=ex_data["correct_answer"],
                options=json.dumps(ex_data["options"]) if ex_data["options"] else None,
                difficulty=ex_data["difficulty"],
                explanation=ex_data["explanation"],
                xp_reward=10,
                order=ex_data["order"]
            )
            db.add(exercise)
        
        db.commit()
        print(f"✅ Создано {len(exercises_lesson2)} упражнений для урока 2")
        
        # 3. Создаём достижения
        print("\n🏆 Создаём достижения...")
        
        achievements = [
            {
                "code": "FIRST_LESSON",
                "name": "Первые шаги",
                "description": "Пройдено первое упражнение",
                "icon": "🎯"
            },
            {
                "code": "WEEK_STREAK",
                "name": "Неделя подряд",
                "description": "Занимались 7 дней подряд",
                "icon": "🔥"
            },
            {
                "code": "HUNDRED_XP",
                "name": "Сотня!",
                "description": "Заработано 100 XP",
                "icon": "⭐",
                "xp_required": 100
            }
        ]
        
        for ach_data in achievements:
            achievement = AchievementModel(**ach_data)
            db.add(achievement)
        
        db.commit()
        print(f"✅ Создано {len(achievements)} достижений")
        
        print("\n✨ База данных успешно заполнена тестовыми данными!")
        print("\n📝 Данные для входа:")
        print("   Email: test@example.com")
        print("   Password: password123")
        
    except Exception as e:
        print(f"\n❌ Ошибка при заполнении БД: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
