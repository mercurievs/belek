# Перенос и установка проекта на другой ноутбук

## 1. Что нужно установить заранее

- Git
- Python 3.11-3.13 (рекомендуется)
- Node.js 18+ и npm

Примечание: с Python 3.14 могут быть несовместимости некоторых версий библиотек. Если используете 3.14, при необходимости обновите SQLAlchemy:

```powershell
pip install "sqlalchemy>=2.0.40"
```

## 2. Склонировать проект

Откройте терминал в папке, где хотите хранить проект, и выполните:

```powershell
git clone https://github.com/mercurievs/belek.git
cd belek
```

## 3. Настройка Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3.1 Заполнить базу данных (рекомендуется)

```powershell
python seed_full_db.py
```

### 3.2 Запустить Backend

```powershell
uvicorn app.main:app --reload
```

Backend будет доступен по адресу:

- <http://localhost:8000>
- Swagger: <http://localhost:8000/docs>

## 4. Настройка Frontend

Откройте второй терминал:

```powershell
cd frontend
npm install
npm run dev
```

Frontend будет доступен по адресу:

- <http://localhost:5173>

## 5. Быстрая проверка

1. Откройте <http://localhost:8000/docs> и убедитесь, что backend работает.
2. Откройте <http://localhost:5173> и убедитесь, что frontend работает.

## 6. Тестовый пользователь (после seed)

- Email: <test@example.com>
- Password: password123

## 7. Команды GitHub для загрузки проекта

Репозиторий назначения:

- <https://github.com/mercurievs/belek.git>

### Вариант A: новый репозиторий из командной строки

```powershell
echo "# belek" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/mercurievs/belek.git
git push -u origin main
```

### Вариант B: отправить изменения в существующий репозиторий

```powershell
git remote add origin https://github.com/mercurievs/belek.git
git branch -M main
git push -u origin main
```

## 8. Если remote origin уже существует

Проверьте текущие remote:

```powershell
git remote -v
```

Если нужно заменить origin:

```powershell
git remote remove origin
git remote add origin https://github.com/mercurievs/belek.git
```

## 9. Частые проблемы

### Ошибка PowerShell при активации venv

Разрешите скрипты для текущего пользователя:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Порт занят

- Backend: поменять порт, например `uvicorn app.main:app --reload --port 8001`
- Frontend: `npm run dev -- --port 5174`
