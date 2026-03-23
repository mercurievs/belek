# 🏗️ Архитектура Frontend-приложения

## 📋 Общая структура

### Принципы организации кода

1. **Разделение по функциям** - каждая папка отвечает за свою область
2. **Переиспользуемость** - компоненты можно использовать многократно
3. **Чистый код** - каждый файл решает одну задачу
4. **Масштабируемость** - легко добавлять новые функции

---

## 📁 Структура папок

```
src/
├── components/       # Переиспользуемые компоненты
├── pages/           # Страницы приложения (роуты)
├── context/         # Глобальное состояние (React Context)
├── services/        # Взаимодействие с API
├── hooks/           # Custom React hooks
└── utils/           # Вспомогательные функции
```

---

## 🧩 Компоненты (components/)

### common/ - Общие UI компоненты

Базовые элементы интерфейса, используемые во всём приложении:

- **Button.jsx** - кнопки с разными вариантами (primary, secondary, disabled)
- **Input.jsx** - поля ввода с валидацией
- **Card.jsx** - карточки для контента
- **Spinner.jsx** - индикатор загрузки
- **Alert.jsx** - уведомления (success, error, info)

### layout/ - Структура приложения

Компоненты, определяющие макет:

- **Header.jsx** - шапка с навигацией и профилем
- **Footer.jsx** - подвал сайта
- **PrivateRoute.jsx** - защита приватных роутов (проверка JWT)

### exercises/ - Компоненты упражнений

Специализированные компоненты для разных типов упражнений:

- **MultipleChoice.jsx** - выбор из вариантов ответа
- **Translation.jsx** - перевод предложений
- **TypeAnswer.jsx** - ввод текста вручную

---

## 📄 Страницы (pages/)

Каждая страница = отдельный роут в приложении:

### Публичные страницы

- **Login.jsx** - `/login` - вход в систему
- **Register.jsx** - `/register` - регистрация

### Приватные страницы (требуют авторизации)

- **Dashboard.jsx** - `/dashboard` - главная с прогрессом, XP, streak
- **Lessons.jsx** - `/lessons` - список всех уроков
- **Lesson.jsx** - `/lessons/:id` - детали урока с описанием
- **Exercise.jsx** - `/exercises/:id` - прохождение упражнения

---

## 🔐 Аутентификация (context/AuthContext.jsx)

### Что делает AuthContext?

Хранит глобальное состояние пользователя и предоставляет функции:

```javascript
{
  user: { id, email, username, level, xp },
  token: "jwt_token_here",
  login: (email, password) => {},
  register: (email, username, password) => {},
  logout: () => {},
  loading: true/false
}
```

### Как работает?

1. При загрузке приложения проверяется `localStorage`
2. Если токен есть → получаем данные пользователя
3. Если токена нет → пользователь не авторизован
4. При login/register → сохраняем токен в `localStorage`
5. При logout → удаляем токен

---

## 🌐 API сервисы (services/)

### api.js - Базовая настройка axios

- URL backend: `http://localhost:8000/api/v1`
- Автоматическое добавление JWT токена в заголовки
- Обработка ошибок 401 (redirect на /login)

### authService.js - Аутентификация

```javascript
login(email, password)        // POST /auth/login
register(email, username, password) // POST /auth/register
getCurrentUser()              // GET /auth/me
```

### lessonService.js - Работа с уроками

```javascript
getLessons()                  // GET /lessons/
getLessonById(id)            // GET /lessons/{id}
```

### exerciseService.js - Упражнения

```javascript
getExercisesByLesson(lessonId) // GET /exercises/lesson/{id}
submitAnswer(exerciseId, answer) // POST /exercises/{id}/submit
```

---

## 🎣 Custom Hooks (hooks/)

### useAuth.js

Хук для использования AuthContext:

```javascript
const { user, login, logout } = useAuth()
```

### useAsync.js

Хук для управления асинхронными операциями:

```javascript
const { data, loading, error, execute } = useAsync(apiFunction)
```

---

## 🛣️ Роутинг

### React Router v6

```javascript
<Routes>
  {/* Публичные */}
  <Route path="/login" element={<Login />} />
  <Route path="/register" element={<Register />} />
  
  {/* Приватные */}
  <Route element={<PrivateRoute />}>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/lessons" element={<Lessons />} />
    <Route path="/lessons/:id" element={<Lesson />} />
    <Route path="/exercises/:id" element={<Exercise />} />
  </Route>
</Routes>
```

### PrivateRoute - защита роутов

Проверяет наличие JWT токена:

- Есть токен → показываем страницу
- Нет токена → редирект на `/login`

---

## 🎨 Стилизация

**Tailwind CSS** - utility-first подход:

```jsx
<button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">
  Войти
</button>
```

Преимущества:

- Быстрая разработка
- Консистентный дизайн
- Адаптивность (responsive)
- Малый размер bundle

---

## 🔄 Поток данных

### 1. Пользователь заходит на сайт

```
main.jsx → App.jsx → AuthProvider проверяет token → Dashboard/Login
```

### 2. Пользователь логинится

```
Login.jsx → authService.login() → Сохранение token → AuthContext обновляется → redirect на /dashboard
```

### 3. Пользователь проходит урок

```
Lessons.jsx → выбор урока → Lesson.jsx (детали) → Exercise.jsx (упражнения) → exerciseService.submitAnswer() → обновление прогресса
```

---

## 📦 Управление состоянием

### Локальное состояние (useState)

Для данных, используемых только внутри компонента:

```javascript
const [answer, setAnswer] = useState('')
```

### Глобальное состояние (Context)

Для данных, нужных всему приложению:

- Информация о пользователе
- JWT токен
- Глобальные настройки

### Серверное состояние (API calls)

Данные с backend:

- Уроки
- Упражнения
- Прогресс

---

## 🚀 План реализации

1. ✅ Настройка роутинга и AuthContext
2. ✅ Создание общих компонентов (Button, Input, Card)
3. ✅ Страницы Login и Register
4. ✅ Dashboard с прогрессом
5. ✅ Список уроков и детали урока
6. ✅ Компоненты упражнений
7. ✅ Обработка ошибок и loading состояний
8. ✅ Тестирование всех функций

---

## 💡 Ключевые концепции для новичков

### Что такое Context?

Способ передавать данные через дерево компонентов без props drilling.

### Что такое Custom Hook?

Функция, которая использует другие hooks и содержит переиспользуемую логику.

### Что такое Private Route?

Компонент, который проверяет авторизацию перед показом страницы.

### Что такое API Service?

Модуль, который инкапсулирует все вызовы к backend API.
