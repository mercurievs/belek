/**
 * Lesson Service
 * Сервис для работы с уроками
 */

import api from './api'

export const lessonService = {
    /**
     * Получить список всех уроков
     * @param {string} level - Фильтр по уровню (опционально)
     * @returns {Promise} Список уроков
     */
    getLessons: async (level = null) => {
        const params = level ? { level } : {}
        const response = await api.get('/lessons/', { params })
        return response.data
    },

    /**
     * Получить детали конкретного урока
     * @param {number} lessonId - ID урока
     * @returns {Promise} Детали урока
     */
    getLessonById: async (lessonId) => {
        const response = await api.get(`/lessons/${lessonId}`)
        return response.data
    }
}

