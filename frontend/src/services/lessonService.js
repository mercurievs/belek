/**
 * Lesson Service
 * Сервис для работы с уроками
 */

import api from './api'

export const lessonService = {
    /**
     * Получить список всех уроков
     * @param {string} level - Фильтр по уровню (опционально)
     * @param {string} language - Язык обучения (ENGLISH или KYRGYZ)
     * @returns {Promise} Список уроков
     */
    getLessons: async (level = null, language = 'ENGLISH') => {
        const params = { language }
        if (level) params.level = level
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

