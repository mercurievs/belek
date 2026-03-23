# 🎓 Платформа изучения английского языка

Полнофункциональная образовательная платформа для изучения английского языка с интерактивными упражнениями, системой прогресса и достижениями.

## ✨ Возможности

### 🎯 Для учащихся

- **Аутентификация**: Регистрация и вход с JWT токенами
- **Персонализированный дашборд**: Отслеживание прогресса, XP и серий
- **20 уроков** по 4 уровням: A1, A2, B1, B2
- **3 типа упражнений**: Multiple Choice, Type Answer, Translation
- **Система XP**: Зарабатывайте опыт за выполнение упражнений
- **Достижения**: 10 уникальных достижений
- **Streak система**: Поддержание ежедневной серии занятий

### 🏆 Геймификация

- Накопление очков опыта (XP)
- Система уровней (A1 → A2 → B1 → B2)
- Отслеживание серий занятий
- Разблокировка достижений

## 📁 Структура проекта

```
eng_curs/
├── ARCHITECTURE.md          # 📐 Детальная архитектура проекта
├── backend/                 # 🔥 Backend (FastAPI + Python)
│   ├── app/
│   │   ├── domain/          # 💎 Доменные модели
│   │   ├── infrastructure/  # 🔧 База данных, репозитории
│   │   ├── services/        # 🧠 Бизнес-логика
│   │   ├── api/             # 🎨 API endpoints
│   │   └── main.py          # Точка входа
│   ├── requirements.txt
│   ├── seed_full_db.py      # Заполнение полными данными
│   └── README.md
└── frontend/                # ⚛️ Frontend (React + Tailwind)
    ├── src/
    │   ├── pages/           # Страницы
    │   ├── components/      # Компоненты
    │   ├── services/        # API клиенты
    │   ├── context/         # State management
    │   └── hooks/           # Custom hooks
    ├── package.json
    └── README.md
```

## 🚀 Быстрый старт

### Backend (FastAPI)

```powershell
# 1. Перейдите в папку backend
cd backend

# 2. Создайте виртуальное окружение
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Заполните БД полными данными (20 уроков, 24 упражнения, 10 достижений)
python seed_full_db.py

# 5. Запустите сервер
uvicorn app.main:app --reload
```

Backend запустится на <http://localhost:8000>

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

### Frontend (React)

```powershell
# 1. Перейдите в папку frontend
cd frontend

# 2. Установите зависимости (уже установлены)
npm install

# 3. Запустите dev server
npm run dev
```

Frontend запустится на <http://localhost:5173>

## 👤 Тестовые данные

После запуска `seed_full_db.py` будет создан тестовый пользователь:

- **Email**: <test@example.com>
- **Password**: password123

### 📊 Статистика базы данных

- 👤 **Пользователей**: 1
- 📚 **Уроков**: 20 (A1: 5, A2: 5, B1: 5, B2: 5)
- ✏️ **Упражнений**: 24 реальных примера
- 🏆 **Достижений**: 10

## 📖 Структура курсов

### A1 (Beginner) - 5 уроков

1. Глагол 'to be' в настоящем времени
2. Личные местоимения
3. Present Simple - утвердительные предложения
4. Артикли: a, an, the
5. Множественное число существительных

### A2 (Elementary) - 5 уроков

6. Past Simple - прошедшее время
2. Future Simple с will
3. Сравнительная степень прилагательных
4. Present Continuous
5. Предлоги времени и места

### B1 (Intermediate) - 5 уроков

11. Present Perfect
2. First Conditional
3. Модальные глаголы
4. Past Continuous
5. Present Perfect Continuous

### B2 (Upper-Intermediate) - 5 уроков

16. Passive Voice
2. Reported Speech
3. Second Conditional
4. Relative Clauses
5. Past Perfect

## 🏗️ Архитектура

Проект построен на основе **Clean Architecture**:

### Backend (4 слоя)

1. **Domain** - Доменные модели (User, Lesson, Exercise)
2. **Infrastructure** - База данных, репозитории, JWT
3. **Application** - Бизнес-логика (Services)
4. **Presentation** - API endpoints (FastAPI)

### Frontend (Структурированный)

1. **Pages** - Страницы приложения
2. **Components** - Переиспользуемые компоненты
3. **Services** - API клиенты
4. **Context** - Глобальное состояние

**Подробнее**: См. [ARCHITECTURE.md](ARCHITECTURE.md)

## 📚 Функциональность

### ✅ Реализовано

#### Backend API

- 🔐 Регистрация и авторизация (JWT)
- 📖 Управление уроками
- ✏️ Система упражнений
- 📊 Отслеживание прогресса
- 🏆 Система XP и достижений
- 🔥 Streak (серия занятий)

#### Типы упражнений

- Multiple Choice (выбор варианта)
- Translation (перевод)
- Type Answer (ввод текста)
- Listening (аудирование) - структура готова

### 🔄 Для дальнейшей разработки

#### Frontend компоненты (структура создана)

- Страница входа/регистрации
- Дашборд с уроками
- Страница урока с упражнениями
- Компоненты для каждого типа упражнений
- Система прогресса и достижений

## 🛠️ Технологии

### Backend

- **FastAPI** - современный веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL/SQLite** - база данных
- **JWT** - аутентификация
- **Pydantic** - валидация данных

### Frontend

- **React 19** - UI библиотека
- **Vite** - сборщик
- **Tailwind CSS** - стили
- **Axios** - HTTP клиент
- **React Router** - маршрутизация

## 📖 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход
- `GET /api/v1/auth/me` - Текущий пользователь

### Lessons

- `GET /api/v1/lessons` - Список уроков
- `GET /api/v1/lessons/{id}` - Детали урока
- `POST /api/v1/lessons/{id}/start` - Начать урок

### Exercises

- `GET /api/v1/exercises/lesson/{id}` - Упражнения урока
- `POST /api/v1/exercises/submit` - Отправить ответ

## 🔒 Безопасность

- ✅ JWT токены
- ✅ Bcrypt хеширование паролей
- ✅ Валидация входных данных
- ✅ CORS настроен
- ✅ SQL Injection защита (через ORM)

## 📝 Следующие шаги

### Для завершения проекта

1. **Frontend компоненты**:
   - Создать страницы Login, Register, Dashboard
   - Реализовать компоненты упражнений
   - Добавить анимации и переходы

2. **Интеграция**:
   - Соединить frontend с backend API
   - Протестировать все flow
   - Обработать ошибки

3. **Дополнительные функции**:
   - Система достижений
   - Статистика прогресса
   - Социальные функции

4. **Деплой**:
   - Backend на Heroku/Railway
   - Frontend на Vercel/Netlify
   - База данных PostgreSQL

## 💡 Примеры использования API

### Регистрация

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","username":"user","password":"password123"}'
```

### Получить уроки

```bash
curl -X GET "http://localhost:8000/api/v1/lessons" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🤝 Разработка

Проект готов для дальнейшей разработки:

- ✅ Архитектура спроектирована
- ✅ Backend полностью реализован
- ✅ Frontend структура создана
- ✅ API endpoints работают
- ✅ База данных настроена
- ✅ Документация написана

## 📧 Контакты

При возникновении вопросов:

1. Изучите [ARCHITECTURE.md](ARCHITECTURE.md)
2. Проверьте Swagger UI на `/docs`
3. Посмотрите примеры в `seed_db.py`

---

**Создано с ❤️ для изучения английского языка**

*Проект демонстрирует современные подходы к разработке full-stack приложений с Clean Architecture*
