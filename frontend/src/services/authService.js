/**
 * Authentication Service
 * Сервис для работы с аутентификацией
 */

import api from './api'

export const authService = {
    /**
     * Регистрация нового пользователя
     * @param {string} email - Email
     * @param {string} username - Имя пользователя
     * @param {string} password - Пароль
     * @returns {Promise} Объект { user, access_token, token_type }
     */
    register: async (email, username, password) => {
        const response = await api.post('/auth/register', {
            email,
            username,
            password
        })
        return response.data
    },

    /**
     * Вход в систему
     * @param {string} email - Email
     * @param {string} password - Пароль
     * @returns {Promise} Объект { user, access_token, token_type }
     */
    login: async (email, password) => {
        const response = await api.post('/auth/login', {
            email,
            password
        })
        return response.data
    },

    /**
     * Получить данные текущего пользователя
     * @returns {Promise} Данные пользователя
     */
    getCurrentUser: async () => {
        const response = await api.get('/auth/me')
        return response.data
    },

    /**
     * Выход из системы (очистка токена)
     */
    logout: () => {
        localStorage.removeItem('token')
    }
}

