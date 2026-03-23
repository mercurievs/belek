import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { Button } from '../common/Button'

/**
 * Header - шапка приложения с навигацией
 * 
 * Показывает:
 * - Логотип
 * - Навигацию (для авторизованных пользователей)
 * - XP и уровень пользователя
 * - Кнопку выхода
 */
export const Header = () => {
    const { user, logout, isAuthenticated } = useAuth()
    const navigate = useNavigate()

    const handleLogout = () => {
        logout()
        navigate('/login')
    }

    return (
        <header className="bg-white shadow-md sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-16">
                    {/* Логотип */}
                    <Link to={isAuthenticated ? '/dashboard' : '/'} className="flex items-center">
                        <span className="text-2xl">🎓</span>
                        <span className="ml-2 text-xl font-bold text-gray-800">
                            English Learning
                        </span>
                    </Link>

                    {/* Навигация (только для авторизованных) */}
                    {isAuthenticated && (
                        <>
                            <nav className="hidden md:flex space-x-8">
                                <Link
                                    to="/dashboard"
                                    className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
                                >
                                    Главная
                                </Link>
                                <Link
                                    to="/lessons"
                                    className="text-gray-700 hover:text-blue-600 font-medium transition-colors"
                                >
                                    Уроки
                                </Link>
                                <Link
                                    to="/practice"
                                    className="text-gray-700 hover:text-purple-600 font-medium transition-colors"
                                >
                                    Практика
                                </Link>
                                <Link
                                    to="/profile"
                                    className="text-gray-700 hover:text-indigo-600 font-medium transition-colors"
                                >
                                    Профиль
                                </Link>
                                {user?.role === 'ADMIN' && (
                                    <Link
                                        to="/admin"
                                        className="text-purple-700 hover:text-purple-900 font-bold transition-colors"
                                    >
                                        🔐 Админ
                                    </Link>
                                )}
                            </nav>

                            {/* Информация о пользователе */}
                            <div className="flex items-center space-x-4">
                                {/* XP и уровень */}
                                <div className="hidden sm:flex items-center space-x-4 text-sm">
                                    <div className="flex items-center">
                                        <span className="text-yellow-500 text-lg mr-1">⭐</span>
                                        <span className="font-semibold text-gray-700">
                                            {user?.total_xp || 0} XP
                                        </span>
                                    </div>
                                    <div className="flex items-center">
                                        <span className="text-blue-500 text-lg mr-1">📊</span>
                                        <span className="font-semibold text-gray-700">
                                            {user?.english_level || 'A1'}
                                        </span>
                                    </div>
                                    <div className="flex items-center">
                                        <span className="text-orange-500 text-lg mr-1">🔥</span>
                                        <span className="font-semibold text-gray-700">
                                            {user?.streak_days || 0}
                                        </span>
                                    </div>
                                </div>

                                {/* Имя пользователя */}
                                <span className="text-gray-700 font-medium">
                                    {user?.username}
                                </span>

                                {/* Кнопка выхода */}
                                <Button
                                    variant="secondary"
                                    onClick={handleLogout}
                                    className="text-sm py-2 px-4"
                                >
                                    Выйти
                                </Button>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </header>
    )
}
