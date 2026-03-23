import { useState, useCallback } from 'react'

/**
 * Custom hook для управления асинхронными операциями
 * 
 * Автоматически управляет состояниями loading, error, data
 * 
 * Пример использования:
 * const { data, loading, error, execute } = useAsync(lessonService.getLessons)
 * 
 * useEffect(() => {
 *   execute()
 * }, [])
 */
export const useAsync = (asyncFunction) => {
    const [loading, setLoading] = useState(false)
    const [data, setData] = useState(null)
    const [error, setError] = useState(null)

    /**
     * Выполнить асинхронную функцию
     */
    const execute = useCallback(async (...params) => {
        try {
            setLoading(true)
            setError(null)

            const result = await asyncFunction(...params)
            setData(result)

            return { success: true, data: result }
        } catch (err) {
            const errorMessage = err.response?.data?.detail || err.message || 'Произошла ошибка'
            setError(errorMessage)

            return { success: false, error: errorMessage }
        } finally {
            setLoading(false)
        }
    }, [asyncFunction])

    /**
     * Сбросить состояние
     */
    const reset = useCallback(() => {
        setLoading(false)
        setData(null)
        setError(null)
    }, [])

    return {
        loading,
        data,
        error,
        execute,
        reset
    }
}
