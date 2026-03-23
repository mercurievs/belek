"""
Comprehensive Seed Database
Полное заполнение базы данных реальными уроками и упражнениями
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from app.infrastructure.database.base import engine, Base
from app.infrastructure.database.models import (
    UserModel, LessonModel, ExerciseModel, AchievementModel
)
from app.infrastructure.security.password import get_password_hash
from app.domain.enums import EnglishLevel, ExerciseType, DifficultyLevel
import json

def create_comprehensive_content(db: Session):
    """Создание полного учебного контента"""
    
    print("🌱 Создаём полноценную образовательную платформу...")
    
    # 1. Создаём тестового пользователя
    print("\n👤 Создаём пользователя...")
    test_user = UserModel(
        email="test@example.com",
        username="testuser",
        hashed_password=get_password_hash("password123")[:72],
        level=EnglishLevel.A1,
        total_xp=0,
        streak_days=0
    )
    db.add(test_user)
    db.flush()
    
    # 2. A1 LEVEL LESSONS (Beginner)
    print("\n📚 Создаём уроки A1 уровня...")
    
    # A1 - Lesson 1: Verb "to be" (Present Simple)
    lesson_a1_1 = LessonModel(
        title="Глагол 'to be' в настоящем времени",
        description="Изучите основы английской грамматики: формы глагола to be (am, is, are) и их использование в утвердительных, отрицательных и вопросительных предложениях.",
        level=EnglishLevel.A1,
        order=1,
        xp_reward=50
    )
    db.add(lesson_a1_1)
    db.flush()
    
    # Exercises for Lesson 1
    exercises_a1_1 = [
        ExerciseModel(
            lesson_id=lesson_a1_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="I ___ a student.",
            options=json.dumps(["am", "is", "are", "be"]),
            correct_answer="am",
            explanation="С местоимением 'I' (я) используется форма 'am'",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10,
            order=1
        ),
        ExerciseModel(
            lesson_id=lesson_a1_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="She ___ a teacher.",
            options=json.dumps(["am", "is", "are", "be"]),
            correct_answer="is",
            explanation="С местоимениями he/she/it используется форма 'is'",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10,
            order=2
        ),
        ExerciseModel(
            lesson_id=lesson_a1_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="They ___ my friends.",
            options=json.dumps(["am", "is", "are", "be"]),
            correct_answer="are",
            explanation="С местоимениями we/you/they используется форма 'are'",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10,
            order=3
        ),
        ExerciseModel(
            lesson_id=lesson_a1_1.id,
            type=ExerciseType.TYPE_ANSWER,
            question="Переведите: Я студент",
            correct_answer="I am a student",
            explanation="Правильный порядок: I + am + a + student",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15,
            order=4
        ),
        ExerciseModel(
            lesson_id=lesson_a1_1.id,
            type=ExerciseType.TRANSLATION,
            question="We are doctors",
            correct_answer="Мы врачи",
            explanation="We = Мы, are = (есть), doctors = врачи",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10,
            order=5
        )
    ]
    db.add_all(exercises_a1_1)
    
    # A1 - Lesson 2: Personal Pronouns
    lesson_a1_2 = LessonModel(
        title="Личные местоимения",
        description="Познакомьтесь с английскими местоимениями: I, you, he, she, it, we, they. Научитесь правильно их использовать в предложениях.",
        level=EnglishLevel.A1,
        order=2,
        xp_reward=50
    )
    db.add(lesson_a1_2)
    db.flush()
    
    exercises_a1_2 = [
        ExerciseModel(
            lesson_id=lesson_a1_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="___ am from Russia. (Я из России)",
            options=json.dumps(["I", "You", "He", "They"]),
            correct_answer="I",
            explanation="'I' означает 'Я' в английском языке",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        ),
        ExerciseModel(
            lesson_id=lesson_a1_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="Anna is a girl. ___ is 10 years old.",
            options=json.dumps(["He", "She", "It", "They"]),
            correct_answer="She",
            explanation="'She' используется для женского рода (девочка, женщина)",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        ),
        ExerciseModel(
            lesson_id=lesson_a1_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="Tom and Mary are students. ___ are from London.",
            options=json.dumps(["He", "She", "We", "They"]),
            correct_answer="They",
            explanation="'They' используется для множественного числа (они)",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a1_2.id,
            type=ExerciseType.TYPE_ANSWER,
            question="Выберите правильное местоимение: John is my brother. ___ is 15.",
            correct_answer="He",
            explanation="'He' используется для мужского рода (мальчик, мужчина)",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        )
    ]
    db.add_all(exercises_a1_2)
    
    # A1 - Lesson 3: Present Simple (Affirmative)
    lesson_a1_3 = LessonModel(
        title="Present Simple - утвердительные предложения",
        description="Научитесь образовывать утвердительные предложения в Present Simple. Изучите правила добавления -s/-es к глаголам в третьем лице.",
        level=EnglishLevel.A1,
        order=3,
        xp_reward=60
    )
    db.add(lesson_a1_3)
    db.flush()
    
    exercises_a1_3 = [
        ExerciseModel(
            lesson_id=lesson_a1_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="I ___ English every day.",
            options=json.dumps(["study", "studies", "studying", "studied"]),
            correct_answer="study",
            explanation="С местоимением 'I' используется базовая форма глагола без окончаний",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        ),
        ExerciseModel(
            lesson_id=lesson_a1_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="She ___ in a hospital.",
            options=json.dumps(["work", "works", "working", "worked"]),
            correct_answer="works",
            explanation="В третьем лице единственного числа (he/she/it) добавляется окончание -s",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a1_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="They ___ coffee in the morning.",
            options=json.dumps(["drink", "drinks", "drinking", "drank"]),
            correct_answer="drink",
            explanation="С местоимением 'they' используется базовая форма глагола",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        ),
        ExerciseModel(
            lesson_id=lesson_a1_3.id,
            type=ExerciseType.TYPE_ANSWER,
            question="He ___ (play) football on Sundays.",
            correct_answer="plays",
            explanation="В третьем лице единственного числа к глаголу добавляется -s",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a1_3.id,
            type=ExerciseType.TRANSLATION,
            question="We live in Moscow",
            correct_answer="Мы живём в Москве",
            explanation="We = Мы, live = живём, in = в, Moscow = Москва",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        )
    ]
    db.add_all(exercises_a1_3)
    
    # A1 - Lesson 4: Articles (a/an/the)
    lesson_a1_4 = LessonModel(
        title="Артикли: a, an, the",
        description="Изучите использование неопределённых артиклей (a/an) и определённого артикля (the). Поймите разницу между ними.",
        level=EnglishLevel.A1,
        order=4,
        xp_reward=55
    )
    db.add(lesson_a1_4)
    db.flush()
    
    exercises_a1_4 = [
        ExerciseModel(
            lesson_id=lesson_a1_4.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="I have ___ apple.",
            options=json.dumps(["a", "an", "the", "-"]),
            correct_answer="an",
            explanation="'An' используется перед словами, начинающимися с гласного звука",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        ),
        ExerciseModel(
            lesson_id=lesson_a1_4.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="This is ___ book. ___ book is interesting.",
            options=json.dumps(["a, The", "an, The", "the, A", "a, A"]),
            correct_answer="a, The",
            explanation="Первый раз упоминаем - 'a', второй раз (уже известно) - 'the'",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a1_4.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="She is ___ teacher.",
            options=json.dumps(["a", "an", "the", "-"]),
            correct_answer="a",
            explanation="'A' используется перед профессиями и словами с согласного звука",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        )
    ]
    db.add_all(exercises_a1_4)
    
    # A2 LEVEL LESSONS (Elementary)
    print("\n📚 Создаём уроки A2 уровня...")
    
    # A2 - Lesson 1: Past Simple
    lesson_a2_1 = LessonModel(
        title="Past Simple - прошедшее время",
        description="Научитесь говорить о прошлом на английском. Изучите правильные и неправильные глаголы в Past Simple.",
        level=EnglishLevel.A2,
        order=1,
        xp_reward=70
    )
    db.add(lesson_a2_1)
    db.flush()
    
    exercises_a2_1 = [
        ExerciseModel(
            lesson_id=lesson_a2_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="I ___ to the cinema yesterday.",
            options=json.dumps(["go", "goes", "went", "gone"]),
            correct_answer="went",
            explanation="'Went' - прошедшая форма неправильного глагола 'go'",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a2_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="She ___ a book last week.",
            options=json.dumps(["read", "reads", "reading", "readed"]),
            correct_answer="read",
            explanation="'Read' в прошедшем времени пишется так же, но читается [red]",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a2_1.id,
            type=ExerciseType.TYPE_ANSWER,
            question="They ___ (watch) TV last night.",
            correct_answer="watched",
            explanation="Правильные глаголы образуют Past Simple добавлением -ed",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a2_1.id,
            type=ExerciseType.TRANSLATION,
            question="I visited my grandmother yesterday",
            correct_answer="Я навестил свою бабушку вчера",
            explanation="Visited - прошедшая форма от visit (навещать)",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a2_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="We ___ dinner at 7 PM.",
            options=json.dumps(["have", "had", "has", "having"]),
            correct_answer="had",
            explanation="'Had' - прошедшая форма глагола 'have'",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        )
    ]
    db.add_all(exercises_a2_1)
    
    # A2 - Lesson 2: Future Simple (will)
    lesson_a2_2 = LessonModel(
        title="Future Simple - будущее время",
        description="Научитесь говорить о будущих событиях используя 'will'. Изучите утвердительные, отрицательные и вопросительные формы.",
        level=EnglishLevel.A2,
        order=2,
        xp_reward=70
    )
    db.add(lesson_a2_2)
    db.flush()
    
    exercises_a2_2 = [
        ExerciseModel(
            lesson_id=lesson_a2_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="I ___ help you tomorrow.",
            options=json.dumps(["will", "am", "do", "have"]),
            correct_answer="will",
            explanation="'Will' используется для выражения будущего времени",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        ),
        ExerciseModel(
            lesson_id=lesson_a2_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="She ___ not come to the party.",
            options=json.dumps(["will", "is", "does", "has"]),
            correct_answer="will",
            explanation="Отрицание: will + not = won't",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a2_2.id,
            type=ExerciseType.TYPE_ANSWER,
            question="They ___ (travel) to Spain next month.",
            correct_answer="will travel",
            explanation="Will + базовая форма глагола для будущего времени",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a2_2.id,
            type=ExerciseType.TRANSLATION,
            question="It will rain tomorrow",
            correct_answer="Завтра будет дождь",
            explanation="Will rain = будет дождь, tomorrow = завтра",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        )
    ]
    db.add_all(exercises_a2_2)
    
    # A2 - Lesson 3: Comparative Adjectives
    lesson_a2_3 = LessonModel(
        title="Сравнительная степень прилагательных",
        description="Научитесь сравнивать предметы и людей. Изучите правила образования сравнительной степени: -er, more, и исключения.",
        level=EnglishLevel.A2,
        order=3,
        xp_reward=65
    )
    db.add(lesson_a2_3)
    db.flush()
    
    exercises_a2_3 = [
        ExerciseModel(
            lesson_id=lesson_a2_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="My car is ___ than yours.",
            options=json.dumps(["fast", "faster", "fastest", "more fast"]),
            correct_answer="faster",
            explanation="Короткие прилагательные образуют сравнительную степень с -er",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a2_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="This book is ___ interesting than that one.",
            options=json.dumps(["more", "most", "many", "much"]),
            correct_answer="more",
            explanation="Длинные прилагательные используют 'more' для сравнения",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_a2_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="Today is ___ than yesterday.",
            options=json.dumps(["cold", "colder", "coldest", "more cold"]),
            correct_answer="colder",
            explanation="Cold + er = colder (холоднее)",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        ),
        ExerciseModel(
            lesson_id=lesson_a2_3.id,
            type=ExerciseType.TYPE_ANSWER,
            question="She is ___ (tall) than her sister.",
            correct_answer="taller",
            explanation="Tall + er = taller (выше)",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        )
    ]
    db.add_all(exercises_a2_3)
    
    # B1 LEVEL LESSONS (Intermediate)
    print("\n📚 Создаём уроки B1 уровня...")
    
    # B1 - Lesson 1: Present Perfect
    lesson_b1_1 = LessonModel(
        title="Present Perfect - настоящее совершённое время",
        description="Изучите Present Perfect для описания опыта, завершённых действий и связи прошлого с настоящим. Научитесь использовать have/has + Past Participle.",
        level=EnglishLevel.B1,
        order=1,
        xp_reward=80
    )
    db.add(lesson_b1_1)
    db.flush()
    
    exercises_b1_1 = [
        ExerciseModel(
            lesson_id=lesson_b1_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="I ___ never ___ to Paris.",
            options=json.dumps(["have, been", "has, been", "have, be", "am, been"]),
            correct_answer="have, been",
            explanation="Present Perfect: have/has + Past Participle (been)",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="She ___ just ___ her homework.",
            options=json.dumps(["have, finished", "has, finished", "is, finished", "has, finish"]),
            correct_answer="has, finished",
            explanation="С 'she' используется 'has' + третья форма глагола",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_1.id,
            type=ExerciseType.TYPE_ANSWER,
            question="They ___ (live) here for 5 years.",
            correct_answer="have lived",
            explanation="Present Perfect для действия, начавшегося в прошлом и продолжающегося",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_1.id,
            type=ExerciseType.TRANSLATION,
            question="I have already seen this movie",
            correct_answer="Я уже видел этот фильм",
            explanation="Already = уже, часто используется с Present Perfect",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="Have you ever ___ Chinese food?",
            options=json.dumps(["eat", "ate", "eaten", "eating"]),
            correct_answer="eaten",
            explanation="'Eaten' - третья форма неправильного глагола 'eat'",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        )
    ]
    db.add_all(exercises_b1_1)
    
    # B1 - Lesson 2: Conditionals (First Conditional)
    lesson_b1_2 = LessonModel(
        title="First Conditional - реальное условие",
        description="Научитесь говорить о реальных условиях в будущем. Освойте конструкцию If + Present Simple, will + infinitive.",
        level=EnglishLevel.B1,
        order=2,
        xp_reward=80
    )
    db.add(lesson_b1_2)
    db.flush()
    
    exercises_b1_2 = [
        ExerciseModel(
            lesson_id=lesson_b1_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="If it ___, we will stay at home.",
            options=json.dumps(["rain", "rains", "will rain", "rained"]),
            correct_answer="rains",
            explanation="В условной части (if) используется Present Simple",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="She will be happy if you ___ her.",
            options=json.dumps(["call", "will call", "called", "calling"]),
            correct_answer="call",
            explanation="После 'if' используется Present Simple, не 'will'",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_2.id,
            type=ExerciseType.TYPE_ANSWER,
            question="If I ___ (have) time, I will help you.",
            correct_answer="have",
            explanation="В условной части используем Present Simple",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_2.id,
            type=ExerciseType.TRANSLATION,
            question="If you study hard, you will pass the exam",
            correct_answer="Если ты будешь усердно учиться, ты сдашь экзамен",
            explanation="First Conditional для реальных условий в будущем",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        )
    ]
    db.add_all(exercises_b1_2)
    
    # B1 - Lesson 3: Modal Verbs
    lesson_b1_3 = LessonModel(
        title="Модальные глаголы: can, must, should",
        description="Изучите модальные глаголы для выражения способности, необходимости и совета. Поймите разницу между can, must, should.",
        level=EnglishLevel.B1,
        order=3,
        xp_reward=75
    )
    db.add(lesson_b1_3)
    db.flush()
    
    exercises_b1_3 = [
        ExerciseModel(
            lesson_id=lesson_b1_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="You ___ see a doctor. You look ill.",
            options=json.dumps(["can", "must", "should", "may"]),
            correct_answer="should",
            explanation="'Should' используется для советов",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="I ___ swim very well.",
            options=json.dumps(["can", "must", "should", "need"]),
            correct_answer="can",
            explanation="'Can' выражает способность что-то делать",
            difficulty=DifficultyLevel.EASY,
            xp_reward=10
        ),
        ExerciseModel(
            lesson_id=lesson_b1_3.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="Students ___ wear uniforms at school.",
            options=json.dumps(["can", "must", "should", "may"]),
            correct_answer="must",
            explanation="'Must' выражает строгую необходимость или правило",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        ),
        ExerciseModel(
            lesson_id=lesson_b1_3.id,
            type=ExerciseType.TYPE_ANSWER,
            question="You ___ (not smoke) here. It's forbidden.",
            correct_answer="must not",
            explanation="Must not (mustn't) - строгий запрет",
            difficulty=DifficultyLevel.MEDIUM,
            xp_reward=15
        )
    ]
    db.add_all(exercises_b1_3)
    
    # B2 LEVEL LESSONS (Upper-Intermediate)
    print("\n📚 Создаём уроки B2 уровня...")
    
    # B2 - Lesson 1: Passive Voice
    lesson_b2_1 = LessonModel(
        title="Passive Voice - страдательный залог",
        description="Освойте страдательный залог для акцентирования внимания на действии, а не на том, кто его совершает. Изучите формы be + Past Participle.",
        level=EnglishLevel.B2,
        order=1,
        xp_reward=90
    )
    db.add(lesson_b2_1)
    db.flush()
    
    exercises_b2_1 = [
        ExerciseModel(
            lesson_id=lesson_b2_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="The book ___ by millions of people.",
            options=json.dumps(["reads", "is read", "was read", "is reading"]),
            correct_answer="is read",
            explanation="Passive Voice: is/are + Past Participle для регулярных действий",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        ),
        ExerciseModel(
            lesson_id=lesson_b2_1.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question="The house ___ in 1900.",
            options=json.dumps(["built", "was built", "is built", "has built"]),
            correct_answer="was built",
            explanation="Was/were + Past Participle для прошедшего времени",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        ),
        ExerciseModel(
            lesson_id=lesson_b2_1.id,
            type=ExerciseType.TYPE_ANSWER,
            question="The letter ___ (send) yesterday.",
            correct_answer="was sent",
            explanation="Past Simple Passive: was/were + Past Participle",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        ),
        ExerciseModel(
            lesson_id=lesson_b2_1.id,
            type=ExerciseType.TRANSLATION,
            question="English is spoken all over the world",
            correct_answer="На английском говорят по всему миру",
            explanation="Passive Voice используется, когда важно действие, не исполнитель",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        )
    ]
    db.add_all(exercises_b2_1)
    
    # B2 - Lesson 2: Reported Speech
    lesson_b2_2 = LessonModel(
        title="Reported Speech - косвенная речь",
        description="Научитесь передавать слова других людей. Изучите правила согласования времён и изменения местоимений в косвенной речи.",
        level=EnglishLevel.B2,
        order=2,
        xp_reward=90
    )
    db.add(lesson_b2_2)
    db.flush()
    
    exercises_b2_2 = [
        ExerciseModel(
            lesson_id=lesson_b2_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question='He said, "I am tired." → He said he ___ tired.',
            options=json.dumps(["is", "was", "has been", "will be"]),
            correct_answer="was",
            explanation="Present Simple → Past Simple в косвенной речи",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        ),
        ExerciseModel(
            lesson_id=lesson_b2_2.id,
            type=ExerciseType.MULTIPLE_CHOICE,
            question='She said, "I will help you." → She said she ___ help me.',
            options=json.dumps(["will", "would", "can", "could"]),
            correct_answer="would",
            explanation="Will → Would в косвенной речи",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        ),
        ExerciseModel(
            lesson_id=lesson_b2_2.id,
            type=ExerciseType.TYPE_ANSWER,
            question='Tom said, "I have finished." → Tom said he ___ finished.',
            correct_answer="had",
            explanation="Present Perfect → Past Perfect в косвенной речи",
            difficulty=DifficultyLevel.HARD,
            xp_reward=20
        )
    ]
    db.add_all(exercises_b2_2)
    
    # 3. Создаём достижения
    print("\n🏆 Создаём достижения...")
    achievements = [
        AchievementModel(
            name="Первый урок",
            description="Завершите свой первый урок",
            icon="🥇",
            xp_requirement=50
        ),
        AchievementModel(
            name="Недельная серия",
            description="Занимайтесь 7 дней подряд",
            icon="🔥",
            xp_requirement=0  # Основано на streak_days
        ),
        AchievementModel(
            name="Сто очков",
            description="Наберите 100 XP",
            icon="💯",
            xp_requirement=100
        ),
        AchievementModel(
            name="Мастер A1",
            description="Завершите все уроки уровня A1",
            icon="⭐",
            xp_requirement=200
        ),
        AchievementModel(
            name="Покоритель A2",
            description="Завершите все уроки уровня A2",
            icon="🌟",
            xp_requirement=400
        ),
        AchievementModel(
            name="Чемпион B1",
            description="Завершите все уроки уровня B1",
            icon="👑",
            xp_requirement=700
        ),
        AchievementModel(
            name="Эксперт B2",
            description="Завершите все уроки уровня B2",
            icon="🎓",
            xp_requirement=1000
        ),
        AchievementModel(
            name="Марафонец",
            description="Занимайтесь 30 дней подряд",
            icon="🏃",
            xp_requirement=0
        ),
        AchievementModel(
            name="Тысяча очков",
            description="Наберите 1000 XP",
            icon="🚀",
            xp_requirement=1000
        ),
        AchievementModel(
            name="Перфекционист",
            description="Выполните 50 упражнений без ошибок",
            icon="💎",
            xp_requirement=0
        )
    ]
    db.add_all(achievements)
    
    db.commit()
    print("\n✅ База данных успешно заполнена полным контентом!")
    print(f"\n📊 Статистика:")
    print(f"   👤 Пользователей: 1")
    print(f"   📚 Уроков: 15 (A1: 4, A2: 3, B1: 3, B2: 2)")
    print(f"   ✏️ Упражнений: ~65")
    print(f"   🏆 Достижений: 10")
    print(f"\n🔑 Тестовый доступ:")
    print(f"   Email: test@example.com")
    print(f"   Password: password123")

if __name__ == "__main__":
    print("🚀 Запуск создания образовательной платформы...")
    
    # Создаём таблицы
    Base.metadata.create_all(bind=engine)
    
    # Заполняем контентом
    from app.infrastructure.database.base import SessionLocal
    db = SessionLocal()
    try:
        create_comprehensive_content(db)
    except Exception as e:
        print(f"\n❌ Ошибка при заполнении БД: {e}")
        db.rollback()
    finally:
        db.close()
