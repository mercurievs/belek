import { createContext, useState, useEffect } from 'react'
import { authService } from '../services/authService'

// Создаём контекст для аутентификации
export const AuthContext = createContext(null)

/**
 * AuthProvider - провайдер контекста аутентификации
 * 
 * Что делает:
 * 1. Хранит данные пользователя и токен
 * 2. Проверяет токен при загрузке приложения
 * 3. Предоставляет функции login/register/logout
 * 4. Автоматически обновляет состояние пользователя
 */
export const AuthProvider = ({ children }) => {
    // Состояния
    const [user, setUser] = useState(null)          // Данные пользователя
    const [loading, setLoading] = useState(true)    // Идёт ли загрузка
    const [error, setError] = useState(null)        // Ошибка аутентификации

    /**
     * При загрузке приложения проверяем токен в localStorage
     */
    useEffect(() => {
        checkAuth()
    }, [])

    /**
     * Проверка аутентификации
     * Если токен есть - получаем данные пользователя
     */
    const checkAuth = async () => {
        try {
            const token = localStorage.getItem('token')

            if (!token) {
                setLoading(false)
                return
            }

            // Получаем данные текущего пользователя
            const userData = await authService.getCurrentUser()
            setUser(userData)
            setError(null)
        } catch (err) {
            console.error('Auth check failed:', err)
            // Если токен невалиден - удаляем его
            localStorage.removeItem('token')
            setUser(null)
        } finally {
            setLoading(false)
        }
    }

    /**
     * Вход в систему
     * @param {string} email - Email пользователя
     * @param {string} password - Пароль
     */
    const login = async (email, password) => {
        try {
            setError(null)
            setLoading(true)

            // Отправляем запрос на backend
            const response = await authService.login(email, password)

            // Сохраняем токен в localStorage
            localStorage.setItem('token', response.access_token)

            // Устанавливаем данные пользователя из ответа
            setUser(response.user)

            return { success: true }
        } catch (err) {
            const errorMessage = err.response?.data?.detail || 'Ошибка входа'
            setError(errorMessage)
            return { success: false, error: errorMessage }
        } finally {
            setLoading(false)
        }
    }

    /**
     * Регистрация нового пользователя
     * @param {string} email - Email
     * @param {string} username - Имя пользователя
     * @param {string} password - Пароль
     */
    const register = async (email, username, password) => {
        try {
            setError(null)
            setLoading(true)

            // Отправляем запрос на backend
            const response = await authService.register(email, username, password)

            // Сохраняем токен
            localStorage.setItem('token', response.access_token)

            // Устанавливаем данные пользователя из ответа
            setUser(response.user)

            return { success: true }
        } catch (err) {
            const errorMessage = err.response?.data?.detail || 'Ошибка регистрации'
            setError(errorMessage)
            return { success: false, error: errorMessage }
        } finally {
            setLoading(false)
        }
    }

    /**
     * Выход из системы
     */
    const logout = () => {
        // Удаляем токен из localStorage
        localStorage.removeItem('token')
        // Очищаем состояние пользователя
        setUser(null)
        setError(null)
    }

    /**
     * Обновление данных пользователя
     * Полезно после изменения профиля или получения XP
     */
    const refreshUser = async () => {
        try {
            const userData = await authService.getCurrentUser()
            setUser(userData)
        } catch (err) {
            console.error('Failed to refresh user:', err)
        }
    }

    // Значения, которые будут доступны всем компонентам
    const value = {
        user,           // Данные пользователя (или null)
        loading,        // true во время загрузки
        error,          // Ошибка (или null)
        login,          // Функция входа
        register,       // Функция регистрации
        logout,         // Функция выхода
        refreshUser,    // Функция обновления данных пользователя
        isAuthenticated: !!user  // true если пользователь залогинен
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}
