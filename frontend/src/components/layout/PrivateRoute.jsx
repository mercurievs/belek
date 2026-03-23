import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'

/**
 * PrivateRoute - защита приватных маршрутов
 * 
 * Проверяет, авторизован ли пользователь:
 * - Если ДА → показываем страницу (Outlet)
 * - Если НЕТ → редирект на /login
 * 
 * Использование в роутинге:
 * <Route element={<PrivateRoute />}>
 *   <Route path="/dashboard" element={<Dashboard />} />
 * </Route>
 */
export const PrivateRoute = () => {
    const { isAuthenticated, loading } = useAuth()

    // Показываем загрузку, пока проверяем токен
    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    <p className="mt-4 text-gray-600">Загрузка...</p>
                </div>
            </div>
        )
    }

    // Если не авторизован → редирект на login
    if (!isAuthenticated) {
        return <Navigate to="/login" replace />
    }

    // Если авторизован → показываем дочерние роуты
    return <Outlet />
}
