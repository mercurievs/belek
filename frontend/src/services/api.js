/**
 * API Configuration
 * Настройка Axios для взаимодействия с backend
 */

import axios from 'axios'

// Базовый URL backend API
const API_BASE_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1')
    .trim()
    .replace(/\/$/, '')

const extraHeaders = {}
if (API_BASE_URL.includes('.loca.lt')) {
    extraHeaders['bypass-tunnel-reminder'] = 'true'
}

// Создаём экземпляр Axios с настройками
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        ...extraHeaders,
    },
})

// Interceptor для добавления JWT токена к каждому запросу
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

// Interceptor для обработки ошибок
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            // Если токен невалиден, очищаем localStorage и перенаправляем на логин
            localStorage.removeItem('token')
            window.location.href = '/login'
        }
        return Promise.reject(error)
    }
)

export default api

