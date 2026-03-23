"""
Extended Database Seeding - Уроки до B2 уровня
Полное заполнение БД уроками от A1 до B2
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.infrastructure.database.base import engine, Base, SessionLocal
from sqlalchemy import text
from app.infrastructure.security.password import get_password_hash
import json

# Импортируем модели
from app.infrastructure.database.models import (
    UserModel, LessonModel, ExerciseModel, 
    AchievementModel, UserProgressModel, ExerciseResultModel
)

def seed_database():
    """Заполнение БД уроками A1-B2"""
    
    db = SessionLocal()
    
    try:
        print("🚀 Начинаем заполнение базы данных (A1-B2)...")
        
        # 1. Создаём пользователя
        print("\n👤 Создаём тестового пользователя...")
        hashed_pwd = get_password_hash("password123")
        db.execute(text("""
            INSERT OR REPLACE INTO users (id, email, username, hashed_password, level, total_xp, streak_days, role, is_active)
            VALUES (1, 'test@example.com', 'testuser', :pwd, 'A1', 0, 0, 'STUDENT', 1)
        """), {"pwd": hashed_pwd})
        
        # 2. Создаём уроки
        print("\n📚 Создаём уроки A1-B2...")
        
        lessons = [
            # ===== A1 LEVEL (5 уроков) =====
            {
                "id": 1, "title": "Глагол 'to be' в настоящем времени",
                "description": "Изучите основы английской грамматики: формы глагола to be",
                "content": "# Глагол 'to be'\n\n- I am\n- You are\n- He/She/It is\n- We are\n- They are",
                "level": "A1", "order": 1, "xp": 50
            },
            {
                "id": 2, "title": "Личные местоимения",
                "description": "Познакомьтесь с английскими местоимениями",
                "content": "# Личные местоимения\n\nI, You, He, She, It, We, They",
                "level": "A1", "order": 2, "xp": 50
            },
            {
                "id": 3, "title": "Present Simple",
                "description": "Настоящее простое время",
                "content": "# Present Simple\n\nI work, He works, They work",
                "level": "A1", "order": 3, "xp": 60
            },
            {
                "id": 4, "title": "Артикли: a, an, the",
                "description": "Изучите использование артиклей",
                "content": "# Артикли\n\na book, an apple, the sun",
                "level": "A1", "order": 4, "xp": 55
            },
            {
                "id": 5, "title": "Множественное число",
                "description": "Образование множественного числа",
                "content": "# Plurals\n\ncat → cats, box → boxes",
                "level": "A1", "order": 5, "xp": 50
            },
            
            # ===== A2 LEVEL (10 уроков) =====
            {
                "id": 6, "title": "Past Simple - правильные глаголы",
                "description": "Прошедшее время с правильными глаголами",
                "content": "# Past Simple\n\nworked, played, watched\nДобавляем -ed к глаголу",
                "level": "A2", "order": 1, "xp": 70
            },
            {
                "id": 7, "title": "Past Simple - неправильные глаголы",
                "description": "Неправильные глаголы в прошедшем времени",
                "content": "# Irregular Verbs\n\ngo → went, see → saw, eat → ate",
                "level": "A2", "order": 2, "xp": 80
            },
            {
                "id": 8, "title": "Future Simple (will)",
                "description": "Будущее время с will",
                "content": "# Future Simple\n\nI will go, She will work",
                "level": "A2", "order": 3, "xp": 70
            },
            {
                "id": 9, "title": "Present Continuous",
                "description": "Настоящее длительное время",
                "content": "# Present Continuous\n\nI am working, She is reading",
                "level": "A2", "order": 4, "xp": 75
            },
            {
                "id": 10, "title": "Степени сравнения прилагательных",
                "description": "Comparative и Superlative",
                "content": "# Comparatives\n\nbig → bigger → the biggest\nbeautiful → more beautiful → the most beautiful",
                "level": "A2", "order": 5, "xp": 80
            },
            {
                "id": 11, "title": "Модальные глаголы: can, could",
                "description": "Модальные глаголы способности",
                "content": "# Modal Verbs: can/could\n\nI can swim, He could run fast",
                "level": "A2", "order": 6, "xp": 70
            },
            {
                "id": 12, "title": "Модальные глаголы: must, should",
                "description": "Модальные глаголы долженствования",
                "content": "# Modal Verbs: must/should\n\nYou must study, We should go",
                "level": "A2", "order": 7, "xp": 70
            },
            {
                "id": 13, "title": "Вопросы в Past Simple",
                "description": "Как задавать вопросы в прошедшем времени",
                "content": "# Questions in Past Simple\n\nDid you go? Did she work?",
                "level": "A2", "order": 8, "xp": 75
            },
            {
                "id": 14, "title": "Предлоги времени и места",
                "description": "Prepositions: in, on, at",
                "content": "# Prepositions\n\nin the morning, on Monday, at 5 o'clock\nin Moscow, on the table, at home",
                "level": "A2", "order": 9, "xp": 70
            },
            {
                "id": 15, "title": "Countable и Uncountable nouns",
                "description": "Исчисляемые и неисчисляемые существительные",
                "content": "# Countable/Uncountable\n\nCountable: apple, book, cat\nUncountable: water, money, information",
                "level": "A2", "order": 10, "xp": 75
            },
            
            # ===== B1 LEVEL (10 уроков) =====
            {
                "id": 16, "title": "Present Perfect",
                "description": "Настоящее совершенное время",
                "content": "# Present Perfect\n\nI have worked, She has seen\nHave/Has + Past Participle (V3)",
                "level": "B1", "order": 1, "xp": 100
            },
            {
                "id": 17, "title": "Present Perfect vs Past Simple",
                "description": "Различия между временами",
                "content": "# Present Perfect vs Past Simple\n\nPresent Perfect: связь с настоящим\nPast Simple: завершенное прошлое",
                "level": "B1", "order": 2, "xp": 110
            },
            {
                "id": 18, "title": "Past Continuous",
                "description": "Прошедшее длительное время",
                "content": "# Past Continuous\n\nI was working, They were playing\nWas/Were + Ving",
                "level": "B1", "order": 3, "xp": 100
            },
            {
                "id": 19, "title": "Passive Voice - Present",
                "description": "Пассивный залог в настоящем времени",
                "content": "# Passive Voice\n\nThe book is written, Cars are made\nam/is/are + V3",
                "level": "B1", "order": 4, "xp": 120
            },
            {
                "id": 20, "title": "Passive Voice - Past",
                "description": "Пассивный залог в прошедшем времени",
                "content": "# Passive Voice (Past)\n\nThe house was built, Letters were sent\nwas/were + V3",
                "level": "B1", "order": 5, "xp": 120
            },
            {
                "id": 21, "title": "First Conditional",
                "description": "Первый тип условных предложений",
                "content": "# First Conditional\n\nIf + Present Simple, will + infinitive\nIf it rains, I will stay home.",
                "level": "B1", "order": 6, "xp": 110
            },
            {
                "id": 22, "title": "Second Conditional",
                "description": "Второй тип условных предложений",
                "content": "# Second Conditional\n\nIf + Past Simple, would + infinitive\nIf I had money, I would buy a car.",
                "level": "B1", "order": 7, "xp": 110
            },
            {
                "id": 23, "title": "Reported Speech",
                "description": "Косвенная речь",
                "content": "# Reported Speech\n\nDirect: 'I am tired'\nReported: He said he was tired",
                "level": "B1", "order": 8, "xp": 120
            },
            {
                "id": 24, "title": "Relative Clauses",
                "description": "Относительные придаточные предложения",
                "content": "# Relative Clauses\n\nwho, which, that, where, when\nThe man who called yesterday...",
                "level": "B1", "order": 9, "xp": 110
            },
            {
                "id": 25, "title": "Gerund vs Infinitive",
                "description": "Герундий и инфинитив",
                "content": "# Gerund vs Infinitive\n\nenjoy + Ving (enjoy swimming)\nwant + to V (want to go)",
                "level": "B1", "order": 10, "xp": 120
            },
            
            # ===== B2 LEVEL (10 уроков) =====
            {
                "id": 26, "title": "Present Perfect Continuous",
                "description": "Настоящее совершенное длительное время",
                "content": "# Present Perfect Continuous\n\nI have been working\nHave/Has + been + Ving",
                "level": "B2", "order": 1, "xp": 150
            },
            {
                "id": 27, "title": "Past Perfect",
                "description": "Прошедшее совершенное время",
                "content": "# Past Perfect\n\nI had finished before you came\nHad + V3",
                "level": "B2", "order": 2, "xp": 150
            },
            {
                "id": 28, "title": "Past Perfect Continuous",
                "description": "Прошедшее совершенное длительное время",
                "content": "# Past Perfect Continuous\n\nI had been working for 3 hours\nHad + been + Ving",
                "level": "B2", "order": 3, "xp": 160
            },
            {
                "id": 29, "title": "Future Perfect",
                "description": "Будущее совершенное время",
                "content": "# Future Perfect\n\nI will have finished by 5 PM\nWill + have + V3",
                "level": "B2", "order": 4, "xp": 150
            },
            {
                "id": 30, "title": "Third Conditional",
                "description": "Третий тип условных предложений",
                "content": "# Third Conditional\n\nIf + Past Perfect, would have + V3\nIf I had known, I would have helped.",
                "level": "B2", "order": 5, "xp": 160
            },
            {
                "id": 31, "title": "Mixed Conditionals",
                "description": "Смешанные условные предложения",
                "content": "# Mixed Conditionals\n\nПрошлое условие + настоящий результат\nIf I had studied, I would be rich now.",
                "level": "B2", "order": 6, "xp": 170
            },
            {
                "id": 32, "title": "Advanced Passive Voice",
                "description": "Пассивный залог в различных временах",
                "content": "# Advanced Passive\n\nPresent Perfect: has been done\nFuture: will be done\nModal: must be done",
                "level": "B2", "order": 7, "xp": 160
            },
            {
                "id": 33, "title": "Wish & If only",
                "description": "Выражение сожаления и желаний",
                "content": "# Wish / If only\n\nI wish I were rich (настоящее)\nI wish I had studied (прошлое)",
                "level": "B2", "order": 8, "xp": 150
            },
            {
                "id": 34, "title": "Phrasal Verbs",
                "description": "Фразовые глаголы продвинутого уровня",
                "content": "# Phrasal Verbs\n\nlook after, give up, carry on, put off\nrun out of, come up with, get over",
                "level": "B2", "order": 9, "xp": 140
            },
            {
                "id": 35, "title": "Advanced Linking Words",
                "description": "Продвинутые связующие слова",
                "content": "# Linking Words\n\nHowever, Moreover, Nevertheless\nFurthermore, Consequently, Therefore",
                "level": "B2", "order": 10, "xp": 140
            },
        ]
        
        for lesson in lessons:
            db.execute(text("""
                INSERT OR REPLACE INTO lessons (id, title, description, content, level, "order", xp_reward, is_published)
                VALUES (:id, :title, :desc, :content, :level, :order, :xp, 1)
            """), {
                "id": lesson["id"],
                "title": lesson["title"],
                "desc": lesson["description"],
                "content": lesson["content"],
                "level": lesson["level"],
                "order": lesson["order"],
                "xp": lesson["xp"]
            })
        
        # 3. Создаём базовые упражнения для каждого урока (по 5 штук для примера)
        print("\n✏️ Создаём базовые упражнения...")
        
        exercise_id = 1
        for lesson_id in range(1, 36):
            level_xp = 10 if lesson_id <= 5 else (15 if lesson_id <= 15 else (20 if lesson_id <= 25 else 25))
            
            # 5 упражнений на каждый урок
            for i in range(1, 6):
                db.execute(text("""
                    INSERT OR REPLACE INTO exercises (
                        id, lesson_id, type, difficulty, question, correct_answer, 
                        options, explanation, xp_reward, "order"
                    )
                    VALUES (:id, :lesson_id, :type, :difficulty, :question, :answer, 
                            :options, :explanation, :xp, :order)
                """), {
                    "id": exercise_id,
                    "lesson_id": lesson_id,
                    "type": "MULTIPLE_CHOICE",
                    "difficulty": "MEDIUM",
                    "question": f"Упражнение {i} для урока {lesson_id}",
                    "answer": "correct",
                    "options": '["correct", "wrong1", "wrong2", "wrong3"]',
                    "explanation": f"Объяснение для упражнения {i}",
                    "xp": level_xp,
                    "order": i
                })
                exercise_id += 1
        
        # 4. Создаём достижения
        print("\n🏆 Создаём достижения...")
        achievements = [
            (1, "FIRST_LESSON", "Первый шаг", "Завершите первый урок", 50, "🥇"),
            (2, "EXERCISES_10", "Практик", "Выполните 10 упражнений", 100, "📝"),
            (3, "STREAK_7", "Недельная серия", "Занимайтесь 7 дней подряд", 200, "🔥"),
            (4, "XP_100", "Столетие", "Наберите 100 XP", 100, "💯"),
            (5, "A1_MASTER", "Мастер A1", "Завершите все уроки A1", 500, "⭐"),
            (6, "A2_MASTER", "Мастер A2", "Завершите все уроки A2", 1000, "🌟"),
            (7, "B1_MASTER", "Мастер B1", "Завершите все уроки B1", 2000, "✨"),
            (8, "B2_MASTER", "Мастер B2", "Завершите все уроки B2", 3000, "💫"),
            (9, "EXERCISES_100", "Профессионал", "Выполните 100 упражнений", 500, "🎯"),
            (10, "XP_1000", "Тысячник", "Наберите 1000 XP", 1000, "🏆"),
        ]
        
        for ach in achievements:
            db.execute(text("""
                INSERT OR REPLACE INTO achievements (id, code, name, description, xp_required, icon)
                VALUES (:id, :code, :name, :desc, :xp, :icon)
            """), {
                "id": ach[0],
                "code": ach[1],
                "name": ach[2],
                "desc": ach[3],
                "xp": ach[4],
                "icon": ach[5]
            })
        
        db.commit()
        
        print("\n" + "="*60)
        print("✅ База данных успешно заполнена!")
        print("="*60)
        print("\n📊 Статистика:")
        print(f"👤 Пользователей: 1")
        print(f"📚 Уроков: 35")
        print(f"   - A1: 5 уроков")
        print(f"   - A2: 10 уроков")
        print(f"   - B1: 10 уроков")
        print(f"   - B2: 10 уроков")
        print(f"✏️ Упражнений: {35 * 5} (по 5 на каждый урок)")
        print(f"🏆 Достижений: 10")
        print("\n🔑 Тестовый аккаунт:")
        print("   Email: test@example.com")
        print("   Password: password123")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("⚠️  Внимание: Эта команда пересоздаст базу данных!")
    print("Все существующие данные будут удалены.\n")
    
    response = input("Продолжить? (yes/no): ")
    if response.lower() != 'yes':
        print("Отменено.")
        exit()
    
    # Пересоздаём таблицы
    print("\n🗑️  Удаляем старые таблицы...")
    Base.metadata.drop_all(bind=engine)
    
    print("🔨 Создаём новые таблицы...")
    Base.metadata.create_all(bind=engine)
    
    # Заполняем данными
    seed_database()
