"""
Заполнение упражнений качественным контентом
Создание упражнений для всех уроков A1-B2
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.infrastructure.database.base import engine, Base, SessionLocal
from sqlalchemy import text

def seed_exercises():
    """Обновление упражнений с качественным контентом"""
    
    db = SessionLocal()
    
    try:
        print("🚀 Обновляем упражнения...")
        
        # Удаляем старые упражнения
        db.execute(text("DELETE FROM exercises"))
        db.commit()
        
        exercises = [
            # ===== УРОК 1: to be (15 упражнений) =====
            (1, 1, "MULTIPLE_CHOICE", "EASY", "I ___ a student.", "am", '["am", "is", "are", "be"]', "С местоимением 'I' используется форма 'am'", 10, 1),
            (2, 1, "MULTIPLE_CHOICE", "EASY", "She ___ a teacher.", "is", '["am", "is", "are", "be"]', "С he/she/it используется 'is'", 10, 2),
            (3, 1, "MULTIPLE_CHOICE", "EASY", "They ___ my friends.", "are", '["am", "is", "are", "be"]', "С they используется 'are'", 10, 3),
            (4, 1, "MULTIPLE_CHOICE", "MEDIUM", "You ___ very kind!", "are", '["am", "is", "are", "be"]', "You всегда с 'are'", 15, 4),
            (5, 1, "TYPE_ANSWER", "MEDIUM", "I ___ happy today. (be)", "am", None, "I am = Я есть (нахожусь в состоянии)", 15, 5),
            (6, 1, "TRANSLATION", "EASY", "We are students", "Мы студенты", None, "We are = Мы есть/являемся", 10, 6),
            (7, 1, "MULTIPLE_CHOICE", "MEDIUM", "It ___ cold outside.", "is", '["am", "is", "are", "be"]', "It используется с 'is'", 15, 7),
            (8, 1, "TYPE_ANSWER", "HARD", "He ___ my brother. (be)", "is", None, "He/She/It + is", 20, 8),
            (9, 1, "MULTIPLE_CHOICE", "EASY", "We ___ at home now.", "are", '["am", "is", "are", "be"]', "We + are", 10, 9),
            (10, 1, "TYPE_ANSWER", "MEDIUM", "She ___ tired. (be)", "is", None, "She + is", 15, 10),
            (11, 1, "TRANSLATION", "MEDIUM", "He is a doctor", "Он врач", None, "He is = Он есть/является", 15, 11),
            (12, 1, "MULTIPLE_CHOICE", "HARD", "I ___ not ready.", "am", '["am", "is", "are", "be"]', "Отрицание: I am not", 20, 12),
            (13, 1, "TYPE_ANSWER", "HARD", "They ___ not here. (be)", "are", None, "They + are not (aren't)", 20, 13),
            (14, 1, "MULTIPLE_CHOICE", "MEDIUM", "The book ___ interesting.", "is", '["am", "is", "are", "be"]', "The book (it) + is", 15, 14),
            (15, 1, "TRANSLATION", "HARD", "I am not tired", "Я не устал", None, "am not = отрицание", 20, 15),
            
            # ===== УРОК 2: Местоимения (15 упражнений) =====
            (16, 2, "MULTIPLE_CHOICE", "EASY", "___ am from Russia.", "I", '["I", "You", "He", "They"]', "'I' = Я", 10, 1),
            (17, 2, "MULTIPLE_CHOICE", "EASY", "Anna is a girl. ___ is 10 years old.", "She", '["He", "She", "It", "They"]', "'She' для женского рода", 10, 2),
            (18, 2, "MULTIPLE_CHOICE", "MEDIUM", "Tom and Kate are friends. ___ are happy.", "They", '["He", "She", "We", "They"]', "'They' для множ. числа", 15, 3),
            (19, 2, "TYPE_ANSWER", "EASY", "John is my friend. ___ is 15.", "He", None, "'He' для мужского рода", 10, 4),
            (20, 2, "MULTIPLE_CHOICE", "MEDIUM", "The dog is hungry. ___ wants food.", "It", '["He", "She", "It", "They"]', "'It' для животных", 15, 5),
            (21, 2, "TRANSLATION", "EASY", "They are happy", "Они счастливы", None, "They = Они", 10, 6),
            (22, 2, "MULTIPLE_CHOICE", "HARD", "___ and I are classmates.", "You", '["I", "You", "We", "They"]', "You = Ты/Вы", 20, 7),
            (23, 2, "TYPE_ANSWER", "MEDIUM", "The car is new. ___ is red.", "It", None, "'It' для предметов", 15, 8),
            (24, 2, "MULTIPLE_CHOICE", "EASY", "My sister and I study together. ___ are students.", "We", '["I", "You", "We", "They"]', "'We' = Мы", 10, 9),
            (25, 2, "TRANSLATION", "MEDIUM", "He is my teacher", "Он мой учитель", None, "He = Он", 15, 10),
            (26, 2, "TYPE_ANSWER", "HARD", "Sarah is a student. ___ studies English.", "She", None, "Sarah = She", 20, 11),
            (27, 2, "MULTIPLE_CHOICE", "MEDIUM", "My parents are doctors. ___ work in a hospital.", "They", '["He", "She", "We", "They"]', "Parents = They", 15, 12),
            (28, 2, "TYPE_ANSWER", "EASY", "___ are very smart!", "You", None, "You = Ты/Вы", 10, 13),
            (29, 2, "TRANSLATION", "HARD", "We are friends", "Мы друзья", None, "We = Мы", 20, 14),
            (30, 2, "MULTIPLE_CHOICE", "HARD", "This is my cat. ___ is very cute.", "It", '["He", "She", "It", "They"]', "Cat = It", 20, 15),
            
            # ===== УРОК 3: Present Simple (15 упражнений) =====
            (31, 3, "MULTIPLE_CHOICE", "EASY", "I ___ English every day.", "study", '["study", "studies", "studying", "studied"]', "I + базовая форма", 10, 1),
            (32, 3, "MULTIPLE_CHOICE", "MEDIUM", "She ___ in an office.", "works", '["work", "works", "working", "worked"]', "She + глагол+s", 15, 2),
            (33, 3, "MULTIPLE_CHOICE", "EASY", "They ___ tea in the morning.", "drink", '["drink", "drinks", "drinking", "drank"]', "They + базовая форма", 10, 3),
            (34, 3, "TYPE_ANSWER", "MEDIUM", "He ___ (play) football on weekends.", "plays", None, "He + глагол+s", 15, 4),
            (35, 3, "TRANSLATION", "EASY", "We live in Moscow", "Мы живём в Москве", None, "Present Simple для фактов", 10, 5),
            (36, 3, "MULTIPLE_CHOICE", "HARD", "My brother ___ to school by bus.", "goes", '["go", "goes", "going", "went"]', "go → goes (после o)", 20, 6),
            (37, 3, "TYPE_ANSWER", "HARD", "They ___ (watch) TV in the evening.", "watch", None, "They + базовая форма", 20, 7),
            (38, 3, "TRANSLATION", "MEDIUM", "He reads books every day", "Он читает книги каждый день", None, "reads = 3 лицо ед.ч.", 15, 8),
            (39, 3, "MULTIPLE_CHOICE", "MEDIUM", "The sun ___ in the east.", "rises", '["rise", "rises", "rising", "rose"]', "The sun (it) + rises", 15, 9),
            (40, 3, "TYPE_ANSWER", "EASY", "We ___ (like) pizza very much.", "like", None, "We + базовая форма", 10, 10),
            (41, 3, "MULTIPLE_CHOICE", "HARD", "She ___ up at 7 o\\'clock.", "wakes", '["wake", "wakes", "waking", "woke"]', "She + wakes", 20, 11),
            (42, 3, "TRANSLATION", "HARD", "They speak English well", "Они хорошо говорят по-английски", None, "speak = говорят", 20, 12),
            (43, 3, "TYPE_ANSWER", "MEDIUM", "My dog ___ (sleep) a lot.", "sleeps", None, "Dog (it) + sleeps", 15, 13),
            (44, 3, "MULTIPLE_CHOICE", "EASY", "You ___ beautiful songs.", "sing", '["sing", "sings", "singing", "sang"]', "You + базовая форма", 10, 14),
            (45, 3, "TYPE_ANSWER", "HARD", "He ___ (teach) mathematics.", "teaches", None, "teach → teaches (ch+es)", 20, 15),
        ]
        
        print(f"\n✏️ Добавляем {len(exercises)} упражнений...")
        
        for ex in exercises:
            db.execute(text("""
                INSERT INTO exercises (
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
        
        db.commit()
        
        print("\n" + "="*60)
        print("✅ Упражнения успешно обновлены!")
        print("="*60)
        print(f"\n📊 Добавлено упражнений: {len(exercises)}")
        print("🎯 Качественные вопросы и ответы для уроков 1-3")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_exercises()
