import { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'

/**
 * Custom hook для использования AuthContext
 * 
 * Пример использования:
 * const { user, login, logout, isAuthenticated } = useAuth()
 * 
 * @returns {Object} Объект с данными и методами аутентификации
 */
export const useAuth = () => {
    const context = useContext(AuthContext)

    if (!context) {
        throw new Error('useAuth must be used within AuthProvider')
    }

    return context
}
