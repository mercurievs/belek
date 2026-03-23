# 🚀 Backend - English Learning Platform

Backend для платформы изучения английского языка, построенный на **FastAPI** с использованием **Clean Architecture**.

## 📋 Технологии

- **Python 3.11+**
- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **PostgreSQL / SQLite** - база данных
- **Pydantic** - валидация данных
- **JWT** - аутентификация
- **Bcrypt** - хеширование паролей

## 🏗️ Архитектура

Проект построен по принципам **Clean Architecture** с разделением на слои:

```
app/
├── domain/              # 💎 Domain Layer - бизнес-модели
├── infrastructure/      # 🔧 Infrastructure - БД, репозитории
├── services/            # 🧠 Application Layer - бизнес-логика
├── api/                 # 🎨 Presentation Layer - API endpoints
└── core/                # ⚙️ Конфигурация
```

Подробнее об архитектуре см. [ARCHITECTURE.md](../ARCHITECTURE.md)

## 🚀 Быстрый старт

### 1. Установка зависимостей

```powershell
# Создайте виртуальное окружение
python -m venv venv

# Активируйте его
.\venv\Scripts\Activate.ps1

# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

Скопируйте `.env.example` в `.env` и настройте:

```powershell
Copy-Item .env.example .env
```

Измените значения в `.env`:

```env
DATABASE_URL=sqlite:///./english_learning.db
SECRET_KEY=your-super-secret-key-change-this
```

### 3. Заполните БД тестовыми данными

```powershell
python seed_db.py
```

Это создаст:

- ✅ Тестового пользователя: `test@example.com` / `password123`
- ✅ 2 урока с упражнениями (A1 уровень)
- ✅ Достижения

### 4. Запустите сервер

```powershell
# Для разработки (с автоперезагрузкой)
uvicorn app.main:app --reload

# Или через Python
python -m app.main
```

Сервер запустится на `http://localhost:8000`

### 5. Откройте документацию API

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## 📚 API Endpoints

### 🔐 Authentication

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/v1/auth/register` | Регистрация |
| POST | `/api/v1/auth/login` | Вход |
| GET | `/api/v1/auth/me` | Текущий пользователь |

### 📖 Lessons

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/v1/lessons` | Список уроков |
| GET | `/api/v1/lessons/{id}` | Детали урока |
| POST | `/api/v1/lessons/{id}/start` | Начать урок |

### ✏️ Exercises

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/api/v1/exercises/lesson/{id}` | Упражнения урока |
| POST | `/api/v1/exercises/submit` | Отправить ответ |

## 🧪 Тестирование API

### Регистрация

```powershell
curl -X POST "http://localhost:8000/api/v1/auth/register" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "password": "password123"
  }'
```

### Вход

```powershell
curl -X POST "http://localhost:8000/api/v1/auth/login" `
  -H "Content-Type: application/json" `
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Скопируйте `access_token` из ответа и используйте в заголовке:

### Получить уроки

```powershell
curl -X GET "http://localhost:8000/api/v1/lessons" `
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 📊 Модели данных

### User (Пользователь)

- `id`, `email`, `username`
- `level` (A1-C1)
- `total_xp`, `streak_days`

### Lesson (Урок)

- `id`, `title`, `description`
- `level`, `order`, `xp_reward`

### Exercise (Упражнение)

- `id`, `lesson_id`, `type`
- `question`, `correct_answer`, `options`
- `difficulty`, `xp_reward`, `explanation`

### UserProgress (Прогресс)

- `user_id`, `lesson_id`, `status`
- `exercises_completed`, `xp_earned`

## 🔒 Безопасность

- ✅ JWT токены для аутентификации
- ✅ Bcrypt для хеширования паролей
- ✅ Валидация всех входных данных
- ✅ CORS настроен для frontend

## 📁 Структура проекта

```
backend/
├── app/
│   ├── api/                    # API endpoints
│   │   └── v1/
│   │       ├── endpoints/      # Роуты
│   │       └── schemas/        # Pydantic схемы
│   ├── services/               # Бизнес-логика
│   ├── domain/                 # Доменные модели
│   ├── infrastructure/         # БД и репозитории
│   │   ├── database/
│   │   ├── repositories/
│   │   └── security/
│   ├── core/                   # Конфигурация
│   └── main.py                 # Точка входа
├── requirements.txt
├── seed_db.py                  # Заполнение БД
└── README.md
```

## 🛠️ Разработка

### Добавить новый endpoint

1. Создайте схемы в `app/api/v1/schemas/`
2. Добавьте бизнес-логику в `app/services/`
3. Создайте endpoint в `app/api/v1/endpoints/`
4. Подключите роутер в `app/api/v1/router.py`

### Добавить новую модель БД

1. Создайте ORM модель в `app/infrastructure/database/models/`
2. Создайте репозиторий в `app/infrastructure/repositories/`
3. Используйте в сервисах

## 📝 Примечания

- **SQLite** используется для разработки
- Для продакшена рекомендуется **PostgreSQL**
- Используйте **Alembic** для миграций в продакшене
- Токены хранятся в памяти клиента (localStorage)

## 🤝 Контакты

При возникновении вопросов - смотрите документацию API на `/docs`

---

**Создано с ❤️ для изучения английского языка**
