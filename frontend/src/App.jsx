import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { PrivateRoute } from './components/layout/PrivateRoute'
import { Header } from './components/layout/Header'
import { Login } from './pages/Login'
import { Register } from './pages/Register'
import { Dashboard } from './pages/Dashboard'
import { Lessons } from './pages/Lessons'
import { Lesson } from './pages/Lesson'
import { Exercises } from './pages/Exercises'
import { Practice } from './pages/Practice'
import { PracticeExercise } from './pages/PracticeExercise'
import { Profile } from './pages/Profile'
import { AdminPanel } from './pages/AdminPanel'
import './index.css'

/**
 * App - главный компонент приложения
 * 
 * Структура:
 * 1. AuthProvider - оборачивает всё приложение, предоставляет контекст аутентификации
 * 2. Router - настройка маршрутизации
 * 3. Header - шапка с навигацией (показывается только для авторизованных)
 * 4. Routes - определение роутов
 * 
 * Публичные роуты:
 * - /login - вход
 * - /register - регистрация
 * 
 * Приватные роуты (требуют авторизации):
 * - /dashboard - главная страница
 * - /lessons - список уроков
 * - /lessons/:id - детали урока
 * - /exercises/:id - прохождение упражнения
 */
function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen">
          {/* Шапка с навигацией */}
          <Header />

          {/* Маршруты */}
          <Routes>
            {/* Редирект с главной на dashboard или login */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* Публичные роуты */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />

            {/* Приватные роуты (требуют авторизации) */}
            <Route element={<PrivateRoute />}>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/lessons" element={<Lessons />} />
              <Route path="/lessons/:id" element={<Lesson />} />
              <Route path="/lessons/:id/exercises" element={<Exercises />} />
              <Route path="/practice" element={<Practice />} />
              <Route path="/practice/:id" element={<PracticeExercise />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/admin" element={<AdminPanel />} />
            </Route>

            {/* 404 - страница не найдена */}
            <Route path="*" element={
              <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                  <h1 className="text-6xl font-bold text-gray-800 mb-4">404</h1>
                  <p className="text-xl text-gray-600">Страница не найдена</p>
                </div>
              </div>
            } />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App

