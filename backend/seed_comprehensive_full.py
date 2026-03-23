"""
Comprehensive Database Seeding - 15 exercises per lesson + lesson content
Полное заполнение БД: по 15 упражнений на урок + теория
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.infrastructure.database.base import engine, Base, SessionLocal
from sqlalchemy import text
from app.infrastructure.security.password import get_password_hash
import json

# Импортируем модели чтобы они зарегистрировались в Base.metadata
from app.infrastructure.database.models import (
    UserModel, LessonModel, ExerciseModel, 
    AchievementModel, UserProgressModel, ExerciseResultModel
)

def seed_database():
    """Заполнение БД полным контентом с теорией"""
    
    db = SessionLocal()
    
    try:
        print("🚀 Начинаем заполнение базы данных...")
        
        # 1. Создаём пользователя
        print("\n👤 Создаём тестового пользователя...")
        hashed_pwd = get_password_hash("password123")
        db.execute(text("""
            INSERT OR REPLACE INTO users (id, email, username, hashed_password, level, total_xp, streak_days, role, is_active)
            VALUES (1, 'test@example.com', 'testuser', :pwd, 'A1', 0, 0, 'STUDENT', 1)
        """), {"pwd": hashed_pwd})
        
        # 2. Создаём уроки с КОНТЕНТОМ
        print("\n📚 Создаём уроки с теоретическим материалом...")
        
        lessons = [
            # A1 Level
            {
                "id": 1,
                "title": "Глагол 'to be' в настоящем времени",
                "description": "Изучите основы английской грамматики: формы глагола to be",
                "content": """
# Глагол 'to be' (быть, являться, находиться)

## Основные формы:
- **I am** (я есть)
- **You are** (ты есть / вы есть)
- **He/She/It is** (он/она/оно есть)
- **We are** (мы есть)
- **They are** (они есть)

## Примеры:
✓ I **am** a student. - Я студент.
✓ She **is** happy. - Она счастлива.
✓ We **are** friends. - Мы друзья.

## Сокращённые формы:
- I'm, you're, he's, she's, it's, we're, they're

## Отрицание:
- I am **not** (I'm not)
- You are **not** (aren't)
- He **is not** (isn't)
                """,
                "level": "A1",
                "order": 1,
                "xp": 50
            },
            {
                "id": 2,
                "title": "Личные местоимения",
                "description": "Познакомьтесь с английскими местоимениями",
                "content": """
# Личные местоимения (Personal Pronouns)

## Местоимения:
| Английский | Русский |
|------------|---------|
| **I** | я |
| **You** | ты, вы |
| **He** | он |
| **She** | она |
| **It** | оно (для предметов/животных) |
| **We** | мы |
| **They** | они |

## Примеры:
✓ **I** am a teacher. - Я учитель.
✓ **He** is my brother. - Он мой брат.
✓ **They** are students. - Они студенты.

## Важно:
- 'It' используется для предметов, животных и абстрактных понятий
- 'You' одинаково для единственного и множественного числа
                """,
                "level": "A1",
                "order": 2,
                "xp": 50
            },
            {
                "id": 3,
                "title": "Present Simple - настоящее простое время",
                "description": "Научитесь образовывать утвердительные предложения",
                "content": """
# Present Simple (Простое настоящее время)

## Образование:
**I/You/We/They** + глагол (базовая форма)
**He/She/It** + глагол + **-s/-es**

## Примеры:
✓ I **work** every day. - Я работаю каждый день.
✓ She **works** in a hospital. - Она работает в больнице.
✓ They **live** in London. - Они живут в Лондоне.

## Окончание -s/-es:
- **-s**: work → work**s**, play → play**s**
- **-es**: watch → watch**es**, go → go**es**
- **-ies**: study → stud**ies**, fly → fl**ies**

## Использование:
✓ Регулярные действия
✓ Факты
✓ Расписания
                """,
                "level": "A1",
                "order": 3,
                "xp": 60
            },
            {
                "id": 4,
                "title": "Артикли: a, an, the",
                "description": "Изучите использование артиклей",
                "content": """
# Артикли (Articles)

## Неопределённые артикли:
**A** / **An** = один, какой-то

### A - перед согласным звуком:
✓ **a** book, **a** car, **a** student

### An - перед гласным звуком:
✓ **an** apple, **an** hour, **an** umbrella

## Определённый артикль:
**The** = этот, тот (конкретный предмет)

✓ This is **a** book. **The** book is red.
✓ I have **an** apple. **The** apple is green.

## Особые случаи:
- Музыкальные инструменты: play **the** guitar
- Уникальные объекты: **the** sun, **the** moon
- Профессии: I am **a** teacher
                """,
                "level": "A1",
                "order": 4,
                "xp": 55
            },
            {
                "id": 5,
                "title": "Множественное число существительных",
                "description": "Научитесь образовывать множественное число",
                "content": """
# Множественное число (Plurals)

## Правило 1: + S
cat → cat**s**
book → book**s**
pen → pen**s**

## Правило 2: + ES (после s, x, ch, sh, o)
box → box**es**
watch → watch**es**
potato → potato**es**

## Правило 3: Y → IES (после согласной)
baby → bab**ies**
city → cit**ies**

## Исключения:
- child → **children**
- man → **men**
- woman → **women**
- tooth → **teeth**
- foot → **feet**
- mouse → **mice**
                """,
                "level": "A1",
                "order": 5,
                "xp": 50
            }
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
        
        # 3. Создаём упражнения (15 на каждый урок)
        print("\n✏️ Создаём упражнения (15 на каждый урок)...")
        
        exercises = [
            # ===== LESSON 1: to be (15 exercises) =====
            (1, 1, "MULTIPLE_CHOICE", "EASY", "I ___ a student.", "am", '["am", "is", "are", "be"]', "С 'I' используется 'am'", 10, 1),
            (2, 1, "MULTIPLE_CHOICE", "EASY", "She ___ a teacher.", "is", '["am", "is", "are", "be"]', "С he/she/it используется 'is'", 10, 2),
            (3, 1, "MULTIPLE_CHOICE", "EASY", "They ___ my friends.", "are", '["am", "is", "are", "be"]', "С they используется 'are'", 10, 3),
            (4, 1, "MULTIPLE_CHOICE", "MEDIUM", "You ___ very tall!", "are", '["am", "is", "are", "be"]', "'You' всегда с 'are'", 15, 4),
            (5, 1, "TYPE_ANSWER", "MEDIUM", "Вставьте: I ___ a doctor.", "am", None, "I + am", 15, 5),
            (6, 1, "TRANSLATION", "EASY", "We are students", "Мы студенты", None, "We are = Мы есть/являемся", 10, 6),
            (7, 1, "MULTIPLE_CHOICE", "MEDIUM", "It ___ cold today.", "is", '["am", "is", "are", "be"]', "'It' используется с 'is'", 15, 7),
            (8, 1, "TYPE_ANSWER", "HARD", "He ___ my best friend.", "is", None, "He/she/it + is", 20, 8),
            (9, 1, "MULTIPLE_CHOICE", "EASY", "We ___ at home.", "are", '["am", "is", "are", "be"]', "We + are", 10, 9),
            (10, 1, "TYPE_ANSWER", "MEDIUM", "She ___ happy.", "is", None, "She + is", 15, 10),
            (11, 1, "TRANSLATION", "MEDIUM", "He is a doctor", "Он врач", None, "He is = Он есть", 15, 11),
            (12, 1, "MULTIPLE_CHOICE", "HARD", "I ___ not tired.", "am", '["am", "is", "are", "be"]', "I am not = отрицание", 20, 12),
            (13, 1, "TYPE_ANSWER", "HARD", "They ___ not ready.", "are", None, "They + are not", 20, 13),
            (14, 1, "MULTIPLE_CHOICE", "MEDIUM", "My sister ___ 10 years old.", "is", '["am", "is", "are", "be"]', "Sister (she) + is", 15, 14),
            (15, 1, "TRANSLATION", "HARD", "I am not a student", "Я не студент", None, "am not = отрицание", 20, 15),
            
            # ===== LESSON 2: Personal Pronouns (15 exercises) =====
            (16, 2, "MULTIPLE_CHOICE", "EASY", "___ am from Russia.", "I", '["I", "You", "He", "They"]', "'I' = Я", 10, 1),
            (17, 2, "MULTIPLE_CHOICE", "EASY", "Anna is a girl. ___ is 10.", "She", '["He", "She", "It", "They"]', "'She' для женского рода", 10, 2),
            (18, 2, "MULTIPLE_CHOICE", "MEDIUM", "Tom and Mary are students. ___ are happy.", "They", '["He", "She", "We", "They"]', "'They' для множ. числа", 15, 3),
            (19, 2, "TYPE_ANSWER", "EASY", "John is my brother. ___ is 15.", "He", None, "'He' для муж. рода", 10, 4),
            (20, 2, "MULTIPLE_CHOICE", "MEDIUM", "The cat is hungry. ___ wants food.", "It", '["He", "She", "It", "They"]', "'It' для животных", 15, 5),
            (21, 2, "TRANSLATION", "EASY", "They are happy", "Они счастливы", None, "They = Они", 10, 6),
            (22, 2, "MULTIPLE_CHOICE", "HARD", "___ and I are friends.", "You", '["I", "You", "We", "They"]', "You = Ты/Вы", 20, 7),
            (23, 2, "TYPE_ANSWER", "MEDIUM", "The book is on the table. ___ is red.", "It", None, "'It' для предметов", 15, 8),
            (24, 2, "MULTIPLE_CHOICE", "EASY", "My mother and I go to school. ___ are together.", "We", '["I", "You", "We", "They"]', "'We' = Мы", 10, 9),
            (25, 2, "TRANSLATION", "MEDIUM", "He is my friend", "Он мой друг", None, "He = Он", 15, 10),
            (26, 2, "TYPE_ANSWER", "HARD", "Sarah is a teacher. ___ teaches English.", "She", None, "Sarah (she)", 20, 11),
            (27, 2, "MULTIPLE_CHOICE", "MEDIUM", "My parents are doctors. ___ work in a hospital.", "They", '["He", "She", "We", "They"]', "Parents = They", 15, 12),
            (28, 2, "TYPE_ANSWER", "EASY", "___ are a good student.", "You", None, "You = Ты/Вы", 10, 13),
            (29, 2, "TRANSLATION", "HARD", "We are teachers", "Мы учителя", None, "We = Мы", 20, 14),
            (30, 2, "MULTIPLE_CHOICE", "HARD", "This is my dog. ___ is very cute.", "It", '["He", "She", "It", "They"]', "Dog = It", 20, 15),
            
            # ===== LESSON 3: Present Simple (15 exercises) =====
            (31, 3, "MULTIPLE_CHOICE", "EASY", "I ___ English every day.", "study", '["study", "studies", "studying", "studied"]', "I + базовая форма", 10, 1),
            (32, 3, "MULTIPLE_CHOICE", "MEDIUM", "She ___ in a hospital.", "works", '["work", "works", "working", "worked"]', "She + глагол-s", 15, 2),
            (33, 3, "MULTIPLE_CHOICE", "EASY", "They ___ coffee.", "drink", '["drink", "drinks", "drinking", "drank"]', "They + базовая форма", 10, 3),
            (34, 3, "TYPE_ANSWER", "MEDIUM", "He ___ (play) football.", "plays", None, "He + глагол-s", 15, 4),
            (35, 3, "TRANSLATION", "EASY", "We live in Moscow", "Мы живём в Москве", None, "Present Simple", 10, 5),
            (36, 3, "MULTIPLE_CHOICE", "HARD", "My sister ___ to school by bus.", "goes", '["go", "goes", "going", "went"]', "После o/s/x → -es", 20, 6),
            (37, 3, "TYPE_ANSWER", "HARD", "They ___ (watch) TV.", "watch", None, "They + базовая форма", 20, 7),
            (38, 3, "TRANSLATION", "MEDIUM", "He reads books", "Он читает книги", None, "reads = 3 лицо ед.ч", 15, 8),
            (39, 3, "MULTIPLE_CHOICE", "MEDIUM", "My brother ___ computer games.", "plays", '["play", "plays", "playing", "played"]', "Brother (he) + -s", 15, 9),
            (40, 3, "TYPE_ANSWER", "EASY", "We ___ (like) pizza.", "like", None, "We + базовая форма", 10, 10),
            (41, 3, "MULTIPLE_CHOICE", "HARD", "She ___ at 7 o\\'clock.", "wakes", '["wake", "wakes", "waking", "woke"]', "She + -s", 20, 11),
            (42, 3, "TRANSLATION", "HARD", "They work hard", "Они много работают", None, "work = работают", 20, 12),
            (43, 3, "TYPE_ANSWER", "MEDIUM", "The cat ___ (sleep) all day.", "sleeps", None, "Cat (it) + -s", 15, 13),
            (44, 3, "MULTIPLE_CHOICE", "EASY", "You ___ very well.", "speak", '["speak", "speaks", "speaking", "spoke"]', "You + базовая форма", 10, 14),
            (45, 3, "TYPE_ANSWER", "HARD", "He ___ (teach) Math.", "teaches", None, "teach → teaches", 20, 15),
            
            # ===== LESSON 4: Articles (15 exercises) =====
            (46, 4, "MULTIPLE_CHOICE", "EASY", "I have ___ apple.", "an", '["a", "an", "the", "-"]', "'An' перед гласным", 10, 1),
            (47, 4, "MULTIPLE_CHOICE", "EASY", "She is ___ teacher.", "a", '["a", "an", "the", "-"]', "'A' перед согласным", 10, 2),
            (48, 4, "MULTIPLE_CHOICE", "MEDIUM", "This is ___ book. ___ book is red.", "a, The", '["a, The", "an, A", "the, A", "-, the"]', "Первое: a, второе: the", 15, 3),
            (49, 4, "TYPE_ANSWER", "MEDIUM", "I want ___ orange.", "an", None, "'An' перед гласным", 15, 4),
            (50, 4, "MULTIPLE_CHOICE", "HARD", "___ sun is bright.", "The", '["A", "An", "The", "-"]', "Уникальные объекты: the", 20, 5),
            (51, 4, "TRANSLATION", "EASY", "I am a doctor", "Я врач", None, "a doctor = врач", 10, 6),
            (52, 4, "MULTIPLE_CHOICE", "MEDIUM", "He plays ___ guitar.", "the", '["a", "an", "the", "-"]', "Инструменты: the", 15, 7),
            (53, 4, "TYPE_ANSWER", "HARD", "She is ___ engineer.", "an", None, "engineer начинается с гласного", 20, 8),
            (54, 4, "MULTIPLE_CHOICE", "EASY", "I see ___ cat.", "a", '["a", "an", "the", "-"]', "Первое упоминание: a", 10, 9),
            (55, 4, "TRANSLATION", "MEDIUM", "The dog is big", "Собака большая", None, "The = конкретная собака", 15, 10),
            (56, 4, "TYPE_ANSWER", "MEDIUM", "There is ___ car.", "a", None, "car: согласный звук", 15, 11),
            (57, 4, "MULTIPLE_CHOICE", "HARD", "I live in ___ house.", "a", '["a", "an", "the", "-"]', "Неопределённый: a", 20, 12),
            (58, 4, "TYPE_ANSWER", "EASY", "___ moon is beautiful.", "The", None, "Уникальный объект: the", 10, 13),
            (59, 4, "TRANSLATION", "HARD", "She is an artist", "Она художница", None, "an artist = художница", 20, 14),
            (60, 4, "MULTIPLE_CHOICE", "MEDIUM", "This is ___ pen.", "a", '["a", "an", "the", "-"]', "Pen: согласный звук", 15, 15),
            
            # ===== LESSON 5: Plurals (15 exercises) =====
            (61, 5, "MULTIPLE_CHOICE", "EASY", "One cat, two ___", "cats", '["cat", "cats", "cates", "caties"]', "Обычное: + s", 10, 1),
            (62, 5, "MULTIPLE_CHOICE", "MEDIUM", "One box, two ___", "boxes", '["boxs", "boxes", "boxies", "boxen"]', "После x: + es", 15, 2),
            (63, 5, "MULTIPLE_CHOICE", "EASY", "One book, three ___", "books", '["book", "books", "bookes", "bookies"]', "Обычное: + s", 10, 3),
            (64, 5, "TYPE_ANSWER", "HARD", "One child, two ___", "children", None, "Исключение: children", 20, 4),
            (65, 5, "MULTIPLE_CHOICE", "MEDIUM", "One class, two ___", "classes", '["classs", "classes", "classies", "classen"]', "После ss: + es", 15, 5),
            (66, 5, "TRANSLATION", "EASY", "Three dogs", "Три собаки", None, "dog → dogs", 10, 6),
            (67, 5, "TYPE_ANSWER", "HARD", "One man, two ___", "men", None, "Исключение: men", 20, 7),
            (68, 5, "MULTIPLE_CHOICE", "MEDIUM", "One baby, two ___", "babies", '["babys", "babies", "babyes", "babyen"]', "y → ies", 15, 8),
            (69, 5, "TYPE_ANSWER", "EASY", "One pen, five ___", "pens", None, "Обычное: + s", 10, 9),
            (70, 5, "TRANSLATION", "MEDIUM", "Two chairs", "Два стула", None, "chair → chairs", 15, 10),
            (71, 5, "MULTIPLE_CHOICE", "HARD", "One tooth, two ___", "teeth", '["tooths", "teeth", "toothes", "toothies"]', "Исключение: teeth", 20, 11),
            (72, 5, "TYPE_ANSWER", "MEDIUM", "One watch, two ___", "watches", None, "После ch: + es", 15, 12),
            (73, 5, "MULTIPLE_CHOICE", "EASY", "One table, two ___", "tables", '["table", "tables", "tablees", "tablies"]', "Обычное: + s", 10, 13),
            (74, 5, "TRANSLATION", "HARD", "Four women", "Четыре женщины", None, "woman → women", 20, 14),
            (75, 5, "TYPE_ANSWER", "HARD", "One mouse, two ___", "mice", None, "Исключение: mice", 20, 15),
        ]
        
        for ex in exercises:
            db.execute(text("""
                INSERT OR REPLACE INTO exercises (
                    id, lesson_id, type, difficulty, question, correct_answer, 
                    options, explanation, xp_reward, "order"
                )
                VALUES (:id, :lesson_id, :type, :difficulty, :question, :answer, 
                        :options, :explanation, :xp, :order)
            """), {
                "id": ex[0],
                "lesson_id": ex[1],
                "type": ex[2],
                "difficulty": ex[3],
                "question": ex[4],
                "answer": ex[5],
                "options": ex[6],
                "explanation": ex[7],
                "xp": ex[8],
                "order": ex[9]
            })
        
        # 4. Создаём достижения
        print("\n🏆 Создаём достижения...")
        achievements = [
            (1, "FIRST_LESSON", "Первый шаг", "Завершите первый урок", 50, "🥇"),
            (2, "EXERCISES_10", "Практик", "Выполните 10 упражнений", 100, "📝"),
            (3, "STREAK_7", "Недельная серия", "Занимайтесь 7 дней подряд", 200, "🔥"),
            (4, "XP_100", "Столетие", "Наберите 100 XP", 100, "💯"),
            (5, "A1_MASTER", "Мастер A1", "Завершите все уроки A1", 500, "⭐"),
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
        
        print("\n" + "="*50)
        print("✅ База данных успешно заполнена!")
        print("="*50)
        print("\n📊 Статистика:")
        print(f"👤 Пользователей: 1")
        print(f"📚 Уроков: 5 (A1 level)")
        print(f"✏️ Упражнений: 75 (15 на каждый урок)")
        print(f"🏆 Достижений: 5")
        print(f"📖 Контент: Теория добавлена к каждому уроку")
        print("\n🔑 Тестовый аккаунт:")
        print("   Email: test@example.com")
        print("   Password: password123")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("⚠️  Внимание: Эта команда пересоздаст базу данных!")
    print("Все существующие данные будут удалены.\n")
    
    # Пересоздаём таблицы
    print("🗑️  Удаляем старые таблицы...")
    Base.metadata.drop_all(bind=engine)
    
    print("🔨 Создаём новые таблицы...")
    Base.metadata.create_all(bind=engine)
    
    # Заполняем данными
    seed_database()
