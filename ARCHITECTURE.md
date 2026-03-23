# 🏗️ АРХИТЕКТУРА ПРОЕКТА: English Learning Platform

## 📊 ОБЩАЯ СТРУКТУРА

```
┌─────────────────────────────────────────────────────────────────┐
│                        ПОЛЬЗОВАТЕЛЬ                              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (React)                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Presentation Layer (UI Components)                      │   │
│  │  - Страницы (Pages)                                      │   │
│  │  - Компоненты (Components)                               │   │
│  │  - Хуки (Hooks)                                          │   │
│  └──────────────────┬───────────────────────────────────────┘   │
│                     │                                            │
│  ┌──────────────────▼───────────────────────────────────────┐   │
│  │  Application Layer (Business Logic)                      │   │
│  │  - Сервисы (Services)                                    │   │
│  │  - Стейт-менеджмент (Context/Redux)                      │   │
│  │  - API клиенты                                           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────┬───────────────────────────────────────────┘
                      │ HTTP/REST API
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI)                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Presentation Layer (API Endpoints)                      │   │
│  │  - Роуты (Routes/Controllers)                            │   │
│  │  - Схемы Pydantic (Request/Response Models)              │   │
│  │  - Middleware (Auth, CORS, Error Handling)               │   │
│  └──────────────────┬───────────────────────────────────────┘   │
│                     │                                            │
│  ┌──────────────────▼───────────────────────────────────────┐   │
│  │  Application Layer (Use Cases)                           │   │
│  │  - Бизнес-логика приложения                              │   │
│  │  - Сервисы (Services)                                    │   │
│  │  - Валидация и обработка данных                          │   │
│  └──────────────────┬───────────────────────────────────────┘   │
│                     │                                            │
│  ┌──────────────────▼───────────────────────────────────────┐   │
│  │  Domain Layer (Core Business Logic)                      │   │
│  │  - Модели домена (Domain Models)                         │   │
│  │  - Бизнес-правила                                        │   │
│  │  - Интерфейсы репозиториев                               │   │
│  └──────────────────┬───────────────────────────────────────┘   │
│                     │                                            │
│  ┌──────────────────▼───────────────────────────────────────┐   │
│  │  Infrastructure Layer (Data & External Services)         │   │
│  │  - Репозитории (Repositories)                            │   │
│  │  - ORM модели (SQLAlchemy)                               │   │
│  │  - Подключение к БД                                      │   │
│  │  - Внешние API                                           │   │
│  └──────────────────┬───────────────────────────────────────┘   │
└─────────────────────┼───────────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────────┐
│               DATABASE (PostgreSQL/SQLite)                       │
│  - Пользователи (Users)                                         │
│  - Курсы и Уроки (Courses & Lessons)                            │
│  - Упражнения (Exercises)                                       │
│  - Прогресс пользователей (User Progress)                       │
│  - Достижения (Achievements)                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 CLEAN ARCHITECTURE: СЛОИ И ИХ РОЛИ

### 1️⃣ **PRESENTATION LAYER (Слой представления)**

**Что это?**  
Это "лицо" приложения — всё, что видит и с чем взаимодействует пользователь.

**Роль:**

- **Frontend**: React компоненты, страницы, формы, кнопки
- **Backend**: API endpoints (роуты), которые принимают HTTP запросы

**Простыми словами:**  
Представьте ресторан. Презентационный слой — это официант, который общается с клиентом, принимает заказ и приносит еду.

**Примеры:**

- Страница входа в систему
- Форма регистрации
- API endpoint `/api/users/login`

**Правило:**  
Этот слой **НЕ СОДЕРЖИТ** бизнес-логики. Он только передаёт данные дальше.

---

### 2️⃣ **APPLICATION LAYER (Слой приложения)**

**Что это?**  
Координатор всех действий — оркестрирует работу приложения.

**Роль:**

- Обрабатывает запросы пользователя
- Вызывает нужные сервисы
- Управляет транзакциями
- Применяет бизнес-логику

**Простыми словами:**  
Это менеджер ресторана, который получает заказ от официанта, координирует работу повара, следит за процессом приготовления.

**Примеры:**

- Сервис авторизации (проверяет пароль, создаёт JWT токен)
- Сервис прохождения урока (проверяет ответы, начисляет XP)
- Сервис расчёта streak

**Правило:**  
Содержит **Use Cases** (сценарии использования) — конкретные действия, которые может делать пользователь.

---

### 3️⃣ **DOMAIN LAYER (Доменный слой)**

**Что это?**  
Сердце приложения — содержит главные бизнес-правила и модели.

**Роль:**

- Определяет сущности (User, Lesson, Exercise)
- Содержит бизнес-правила (например, "урок A2 нельзя пройти без прохождения A1")
- Не зависит от фреймворков и технологий

**Простыми словами:**  
Это рецепты и стандарты качества ресторана. Они не меняются от того, кто повар или какая плита используется.

**Примеры:**

- Модель User с полями: id, email, level, xp, streak
- Правило: "За правильный ответ дается 10 XP"
- Правило: "Streak увеличивается, если пользователь занимается каждый день"

**Правило:**  
Самый независимый слой. Не знает ни о базе данных, ни об API, ни о фреймворках.

---

### 4️⃣ **INFRASTRUCTURE LAYER (Инфраструктурный слой)**

**Что это?**  
Технические детали — всё, что связано с "внешним миром".

**Роль:**

- Работа с базой данных (SQL запросы)
- Подключение к внешним API
- Файловая система
- Email рассылки

**Простыми словами:**  
Это склад и поставщики ресторана. Они хранят продукты и обеспечивают кухню всем необходимым.

**Примеры:**

- Репозиторий UserRepository для работы с БД
- Email сервис для отправки писем
- SQLAlchemy ORM модели

**Правило:**  
Этот слой **зависит** от конкретных технологий (PostgreSQL, AWS, etc.), но другие слои от него **не зависят**.

---

## 📂 ИДЕАЛЬНАЯ СТРУКТУРА ПАПОК

```
eng_curs/
│
├── backend/                          # Backend приложение (FastAPI)
│   ├── app/
│   │   ├── __init__.py
│   │   │
│   │   ├── main.py                   # Точка входа FastAPI приложения
│   │   │
│   │   ├── api/                      # 🎨 PRESENTATION LAYER
│   │   │   ├── __init__.py
│   │   │   ├── deps.py               # Зависимости (get_current_user, get_db)
│   │   │   │
│   │   │   ├── v1/                   # API версия 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py         # Главный роутер
│   │   │   │   │
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── auth.py       # Роуты: регистрация, логин
│   │   │   │   │   ├── users.py      # Роуты: профиль, прогресс
│   │   │   │   │   ├── lessons.py    # Роуты: список уроков
│   │   │   │   │   ├── exercises.py  # Роуты: упражнения
│   │   │   │   │   └── progress.py   # Роуты: сохранение прогресса
│   │   │   │   │
│   │   │   │   └── schemas/          # Pydantic схемы (запросы/ответы)
│   │   │   │       ├── __init__.py
│   │   │   │       ├── user.py
│   │   │   │       ├── lesson.py
│   │   │   │       ├── exercise.py
│   │   │   │       └── progress.py
│   │   │
│   │   ├── services/                 # 🧠 APPLICATION LAYER
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py       # Логика авторизации
│   │   │   ├── user_service.py       # Логика работы с пользователями
│   │   │   ├── lesson_service.py     # Логика уроков
│   │   │   ├── exercise_service.py   # Проверка ответов, начисление XP
│   │   │   └── progress_service.py   # Расчет прогресса, streak
│   │   │
│   │   ├── domain/                   # 💎 DOMAIN LAYER
│   │   │   ├── __init__.py
│   │   │   ├── models.py             # Доменные модели (Python классы)
│   │   │   └── enums.py              # Перечисления (LEVEL, EXERCISE_TYPE)
│   │   │
│   │   ├── infrastructure/           # 🔧 INFRASTRUCTURE LAYER
│   │   │   ├── __init__.py
│   │   │   │
│   │   │   ├── database/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py           # Базовые настройки БД
│   │   │   │   ├── session.py        # Сессия SQLAlchemy
│   │   │   │   │
│   │   │   │   └── models/           # ORM модели (SQLAlchemy)
│   │   │   │       ├── __init__.py
│   │   │   │       ├── user.py
│   │   │   │       ├── lesson.py
│   │   │   │       ├── exercise.py
│   │   │   │       └── progress.py
│   │   │   │
│   │   │   ├── repositories/         # Репозитории (работа с БД)
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user_repository.py
│   │   │   │   ├── lesson_repository.py
│   │   │   │   ├── exercise_repository.py
│   │   │   │   └── progress_repository.py
│   │   │   │
│   │   │   └── security/             # JWT, хеширование паролей
│   │   │       ├── __init__.py
│   │   │       ├── jwt.py
│   │   │       └── password.py
│   │   │
│   │   ├── core/                     # Конфигурация
│   │   │   ├── __init__.py
│   │   │   ├── config.py             # Настройки (DB_URL, SECRET_KEY)
│   │   │   └── constants.py          # Константы (XP_PER_EXERCISE)
│   │   │
│   │   └── utils/                    # Вспомогательные функции
│   │       ├── __init__.py
│   │       └── helpers.py
│   │
│   ├── migrations/                   # Alembic миграции БД
│   │   └── versions/
│   │
│   ├── tests/                        # Тесты
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   └── test_lessons.py
│   │
│   ├── requirements.txt              # Python зависимости
│   ├── .env.example                  # Пример переменных окружения
│   └── README.md
│
├── frontend/                         # Frontend приложение (React)
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   │       ├── images/
│   │       └── sounds/
│   │
│   ├── src/
│   │   ├── App.jsx                   # Главный компонент
│   │   ├── main.jsx                  # Точка входа
│   │   │
│   │   ├── pages/                    # 🎨 PRESENTATION: Страницы
│   │   │   ├── Home.jsx              # Главная страница
│   │   │   ├── Login.jsx             # Страница входа
│   │   │   ├── Register.jsx          # Страница регистрации
│   │   │   ├── Dashboard.jsx         # Дашборд пользователя
│   │   │   ├── Lesson.jsx            # Страница урока
│   │   │   └── Profile.jsx           # Профиль пользователя
│   │   │
│   │   ├── components/               # 🎨 PRESENTATION: Компоненты
│   │   │   ├── common/               # Общие компоненты
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Input.jsx
│   │   │   │   ├── Card.jsx
│   │   │   │   ├── ProgressBar.jsx
│   │   │   │   └── Modal.jsx
│   │   │   │
│   │   │   ├── layout/               # Компоненты макета
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   └── Sidebar.jsx
│   │   │   │
│   │   │   └── exercises/            # Компоненты упражнений
│   │   │       ├── MultipleChoice.jsx
│   │   │       ├── Translation.jsx
│   │   │       ├── TypeAnswer.jsx
│   │   │       └── Listening.jsx
│   │   │
│   │   ├── services/                 # 🧠 APPLICATION: Сервисы
│   │   │   ├── api.js                # Axios конфигурация
│   │   │   ├── authService.js        # API вызовы для auth
│   │   │   ├── lessonService.js      # API вызовы для уроков
│   │   │   └── userService.js        # API вызовы для пользователей
│   │   │
│   │   ├── context/                  # 🧠 APPLICATION: State Management
│   │   │   ├── AuthContext.jsx       # Контекст авторизации
│   │   │   ├── LessonContext.jsx     # Контекст урока
│   │   │   └── UserContext.jsx       # Контекст пользователя
│   │   │
│   │   ├── hooks/                    # Custom hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useLesson.js
│   │   │   └── useProgress.js
│   │   │
│   │   ├── utils/                    # Утилиты
│   │   │   ├── validators.js
│   │   │   └── helpers.js
│   │   │
│   │   └── styles/                   # Стили
│   │       ├── globals.css
│   │       └── tailwind.css
│   │
│   ├── package.json
│   ├── tailwind.config.js
│   ├── vite.config.js
│   └── README.md
│
└── README.md                         # Главный README проекта
```

---

## 🔄 ПОТОК ДАННЫХ: От пользователя до базы данных

### Пример: Пользователь проходит упражнение

```
1. ПОЛЬЗОВАТЕЛЬ
   ↓
   Нажимает кнопку "Проверить ответ"

2. FRONTEND - Presentation Layer
   ↓
   Компонент MultipleChoice.jsx отправляет ответ

3. FRONTEND - Application Layer
   ↓
   exerciseService.js делает POST запрос к API
   POST /api/v1/exercises/{exercise_id}/submit
   Body: { "answer": "B" }

4. BACKEND - Presentation Layer (API)
   ↓
   Router exercises.py получает запрос
   Валидирует данные через Pydantic схему

5. BACKEND - Application Layer
   ↓
   exercise_service.py обрабатывает ответ:
   - Проверяет правильность ответа
   - Вызывает progress_service для начисления XP
   - Обновляет streak пользователя

6. BACKEND - Domain Layer
   ↓
   Применяются бизнес-правила:
   - Правильный ответ = +10 XP
   - Неправильный ответ = +0 XP, но попытка засчитана
   - Проверка условий для разблокировки следующего урока

7. BACKEND - Infrastructure Layer
   ↓
   progress_repository.py сохраняет данные в БД через SQLAlchemy:
   - UPDATE user_progress SET xp = xp + 10
   - INSERT INTO exercise_results (...)

8. DATABASE
   ↓
   PostgreSQL сохраняет данные

9. BACKEND → FRONTEND
   ↓
   Возвращается JSON ответ:
   {
     "correct": true,
     "xp_earned": 10,
     "new_total_xp": 150,
     "streak": 5,
     "message": "Отлично! Правильный ответ!"
   }

10. FRONTEND - Application Layer
    ↓
    exerciseService.js получает ответ
    Обновляет состояние в LessonContext

11. FRONTEND - Presentation Layer
    ↓
    Компонент MultipleChoice.jsx:
    - Показывает зелёную анимацию
    - Отображает "+10 XP"
    - Обновляет прогресс-бар
```

---

## 🎓 КЛЮЧЕВЫЕ ПРИНЦИПЫ

### 1. **Dependency Inversion (Инверсия зависимостей)**

Высокоуровневые модули не зависят от низкоуровневых. Оба зависят от абстракций.

**Пример:**

```python
# ❌ ПЛОХО: Сервис напрямую знает о БД
class UserService:
    def get_user(self, user_id):
        db = PostgreSQL()  # Жесткая зависимость!
        return db.query("SELECT * FROM users WHERE id = ?", user_id)

# ✅ ХОРОШО: Сервис зависит от интерфейса
class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def get_user(self, user_id):
        return self.user_repository.find_by_id(user_id)
```

### 2. **Single Responsibility (Единственная ответственность)**

Каждый модуль/класс отвечает только за одну вещь.

**Пример:**

```python
# ❌ ПЛОХО: Один класс делает всё
class User:
    def save_to_db(self): pass
    def send_email(self): pass
    def calculate_xp(self): pass

# ✅ ХОРОШО: Разделены обязанности
class User:  # Только данные
    pass

class UserRepository:  # Только работа с БД
    def save(self, user): pass

class EmailService:  # Только отправка email
    def send(self, to, message): pass

class XPCalculator:  # Только расчёт XP
    def calculate(self, user): pass
```

### 3. **Separation of Concerns (Разделение ответственности)**

Каждый слой решает свою задачу и не вмешивается в другие.

---

## 🚀 ПРЕИМУЩЕСТВА ТАКОЙ АРХИТЕКТУРЫ

### ✅ Масштабируемость

Можно легко добавлять новые функции без изменения существующего кода.

### ✅ Тестируемость

Каждый слой можно тестировать независимо.

### ✅ Поддерживаемость

Новый разработчик легко поймёт, где что находится.

### ✅ Гибкость

Можно заменить PostgreSQL на MongoDB без изменения бизнес-логики.

### ✅ Переиспользование

Бизнес-логику можно использовать в веб, мобильном приложении, CLI.

---

## 📚 СЛОВАРЬ ТЕРМИНОВ

- **Domain** — предметная область (в нашем случае: обучение английскому)
- **Entity** — сущность (User, Lesson, Exercise)
- **Use Case** — сценарий использования (Регистрация, Прохождение урока)
- **Repository** — паттерн для работы с БД (абстракция над SQL)
- **Service** — класс с бизнес-логикой
- **DTO** (Data Transfer Object) — объект для передачи данных между слоями
- **ORM** — Object-Relational Mapping (SQLAlchemy)
- **Middleware** — промежуточный обработчик запросов
- **Dependency Injection** — внедрение зависимостей

---

**Эта архитектура — фундамент профессионального приложения корпоративного уровня! 🎉**
