/**
 * Exercise Service
 * Сервис для работы с упражнениями
 */

import api from './api'

export const exerciseService = {
    /**
     * Получить все упражнения
     * @returns {Promise} Список всех упражнений
     */
    getExercises: async () => {
        const response = await api.get('/exercises')
        return response.data
    },

    /**
     * Получить упражнение по ID
     * @param {number} exerciseId - ID упражнения
     * @returns {Promise} Упражнение
     */
    getExerciseById: async (exerciseId) => {
        const response = await api.get(`/exercises/${exerciseId}`)
        return response.data
    },

    /**
     * Получить упражнения урока
     * @param {number} lessonId - ID урока
     * @returns {Promise} Список упражнений
     */
    getExercisesByLesson: async (lessonId) => {
        const response = await api.get(`/exercises/lesson/${lessonId}`)
        return response.data
    },

    /**
     * Отправить ответ на упражнение (старый метод)
     * @param {number} exerciseId - ID упражнения
     * @param {string} answer - Ответ пользователя
     * @returns {Promise} Результат проверки { correct, xp_earned, explanation }
     */
    submitAnswer: async (exerciseId, answer) => {
        try {
            const response = await api.post(`/exercises/${exerciseId}/submit`, {
                user_answer: answer
            })
            return {
                correct: response.data.is_correct,
                xp_earned: response.data.xp_earned,
                explanation: response.data.explanation,
                correct_answer: response.data.correct_answer
            }
        } catch (error) {
            console.error('Error submitting answer:', error)
            throw error
        }
    },

    /**
     * Отправить упражнение (новый метод для практики)
     * @param {number} exerciseId - ID упражнения
     * @param {string} answer - Ответ пользователя
     * @returns {Promise} Результат проверки
     */
    submitExercise: async (exerciseId, answer) => {
        try {
            const response = await api.post(`/exercises/${exerciseId}/submit`, {
                user_answer: answer
            })
            return {
                correct: response.data.is_correct,
                xp_earned: response.data.xp_earned,
                explanation: response.data.explanation,
                correct_answer: response.data.correct_answer
            }
        } catch (error) {
            console.error('Error submitting exercise:', error)
            throw error
        }
    }
}

