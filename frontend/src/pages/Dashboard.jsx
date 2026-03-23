import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Card } from '../components/common/Card'
import { Spinner } from '../components/common/Spinner'

/**
 * Dashboard - главная страница пользователя
 * 
 * Отображает:
 * - Приветствие с именем пользователя
 * - Статистику: XP, уровень, streak
 * - Прогресс до следующего уровня
 * - Достижения (заглушка пока)
 * - Быстрый доступ к урокам
 */
export const Dashboard = () => {
    const { user, loading, refreshUser } = useAuth()

    useEffect(() => {
        // Обновляем данные пользователя при загрузке
        refreshUser()
    }, [])

    if (loading || !user) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" text="Загрузка..." />
            </div>
        )
    }

    // Вычисляем прогресс до следующего уровня
    // Для простоты: каждые 100 XP = новый уровень
    const currentLevelXP = Math.floor(user.total_xp / 100) * 100
    const nextLevelXP = currentLevelXP + 100
    const progressPercent = ((user.total_xp - currentLevelXP) / 100) * 100

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 relative overflow-hidden">
            {/* Анимированные декоративные элементы */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
                <div className="absolute top-10 left-10 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
                <div className="absolute top-20 right-10 w-72 h-72 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
                <div className="absolute -bottom-10 left-1/2 w-72 h-72 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
            </div>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
                {/* Приветствие с анимацией */}
                <div className="mb-8 animate-fadeIn">
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                        Привет, {user.username}! 👋
                    </h1>
                    <p className="text-xl text-gray-600">
                        Продолжайте изучать английский язык каждый день
                    </p>
                </div>

                {/* Статистика с градиентами */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    {/* XP - золотой градиент */}
                    <Card className="text-center bg-gradient-to-br from-yellow-400 to-orange-500 text-white transform hover:scale-105 transition-transform duration-300 shadow-xl">
                        <div className="text-6xl mb-3">⭐</div>
                        <h3 className="text-4xl font-bold mb-1">
                            {user.total_xp}
                        </h3>
                        <p className="text-white opacity-90 font-medium">Всего XP</p>
                    </Card>

                    {/* Уровень - синий градиент */}
                    <Card className="text-center bg-gradient-to-br from-blue-500 to-indigo-600 text-white transform hover:scale-105 transition-transform duration-300 shadow-xl">
                        <div className="text-6xl mb-3">📊</div>
                        <h3 className="text-4xl font-bold mb-1">
                            {user.english_level || 'A1'}
                        </h3>
                        <p className="text-white opacity-90 font-medium">Уровень английского</p>
                    </Card>

                    {/* Streak - огненный градиент */}
                    <Card className="text-center bg-gradient-to-br from-red-500 to-pink-600 text-white transform hover:scale-105 transition-transform duration-300 shadow-xl">
                        <div className="text-6xl mb-3">🔥</div>
                        <h3 className="text-4xl font-bold mb-1">
                            {user.streak_days || 0}
                        </h3>
                        <p className="text-white opacity-90 font-medium">Дней подряд</p>
                    </Card>
                </div>

                {/* Прогресс с градиентом */}
                <Card className="mb-8 bg-gradient-to-br from-white to-blue-50 shadow-lg">
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4 flex items-center gap-2">
                        <span>📈</span> Прогресс до следующего уровня
                    </h2>
                    <div className="space-y-3">
                        <div className="flex justify-between text-sm font-semibold text-gray-600">
                            <span>{currentLevelXP} XP</span>
                            <span className="text-blue-600">{user.total_xp} XP</span>
                            <span>{nextLevelXP} XP</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-6 shadow-inner">
                            <div
                                className="bg-gradient-to-r from-blue-500 to-purple-600 h-6 rounded-full transition-all duration-500 shadow-lg flex items-center justify-end pr-3"
                                style={{ width: `${progressPercent}%` }}
                            >
                                <span className="text-white text-xs font-bold">{Math.round(progressPercent)}%</span>
                            </div>
                        </div>
                        <p className="text-center text-gray-700 font-semibold text-lg">
                            🎯 Ещё {nextLevelXP - user.total_xp} XP до следующего уровня!
                        </p>
                    </div>
                </Card>

                {/* Достижения с эффектами */}
                <Card className="mb-8 bg-gradient-to-br from-purple-50 to-pink-50 shadow-lg">
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-4 flex items-center gap-2">
                        <span>🏆</span> Достижения
                    </h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {/* Активное достижение */}
                        <div className="text-center p-4 bg-gradient-to-br from-yellow-100 to-yellow-200 rounded-xl shadow-md transform hover:scale-110 transition-transform duration-300 border-2 border-yellow-400">
                            <div className="text-5xl mb-2 animate-bounce">🥇</div>
                            <p className="text-sm font-bold text-gray-800">Первый урок</p>
                            <p className="text-xs text-gray-600 mt-1">Получено!</p>
                        </div>

                        {/* Будущие достижения */}
                        <div className="text-center p-4 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl opacity-60 hover:opacity-100 transition-opacity duration-300">
                            <div className="text-5xl mb-2">🔥</div>
                            <p className="text-sm font-bold text-gray-700">Недельная серия</p>
                            <p className="text-xs text-gray-500 mt-1">7 дней</p>
                        </div>

                        <div className="text-center p-4 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl opacity-60 hover:opacity-100 transition-opacity duration-300">
                            <div className="text-5xl mb-2">💯</div>
                            <p className="text-sm font-bold text-gray-700">Сто очков</p>
                            <p className="text-xs text-gray-500 mt-1">100 XP</p>
                        </div>

                        <div className="text-center p-4 bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl opacity-60 hover:opacity-100 transition-opacity duration-300">
                            <div className="text-5xl mb-2">⭐</div>
                            <p className="text-sm font-bold text-gray-700">Мастер A1</p>
                            <p className="text-xs text-gray-500 mt-1">Все уроки A1</p>
                        </div>
                    </div>
                </Card>

                {/* Действия с анимацией */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <Link to="/lessons" className="block group">
                        <Card className="text-center bg-gradient-to-br from-blue-500 to-indigo-600 text-white hover:shadow-2xl transform hover:scale-105 transition-all duration-300">
                            <div className="text-7xl mb-4 group-hover:animate-bounce">📖</div>
                            <h3 className="text-3xl font-bold mb-2">
                                Начать урок
                            </h3>
                            <p className="opacity-90 text-lg">
                                Изучайте новые слова и грамматику
                            </p>
                        </Card>
                    </Link>

                    <Link to="/practice" className="block group">
                        <Card className="text-center bg-gradient-to-br from-purple-500 to-pink-600 text-white hover:shadow-2xl transform hover:scale-105 transition-all duration-300">
                            <div className="text-7xl mb-4 group-hover:animate-pulse">✏️</div>
                            <h3 className="text-3xl font-bold mb-2">
                                Практика
                            </h3>
                            <p className="opacity-90 text-lg">
                                Закрепите знания упражнениями
                            </p>
                        </Card>
                    </Link>
                </div>
            </div>
        </div>
    )
}
