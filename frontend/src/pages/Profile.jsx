import { useEffect, useState } from 'react'
import { useAuth } from '../hooks/useAuth'
import { Card } from '../components/common/Card'
import { Spinner } from '../components/common/Spinner'

/**
 * Profile - страница профиля пользователя (личный кабинет)
 */
export const Profile = () => {
    const { user, loading, refreshUser } = useAuth()
    const [stats, setStats] = useState(null)

    useEffect(() => {
        refreshUser()
        loadUserStats()
    }, [])

    /**
     * Загрузка статистики пользователя
     */
    const loadUserStats = () => {
        if (!user) return

        // Вычисляем статистику
        const currentLevel = Math.floor(user.total_xp / 100) + 1
        const xpToNextLevel = (currentLevel * 100) - user.total_xp
        const completionRate = user.exercises_completed ?
            Math.round((user.exercises_completed / 81) * 100) : 0

        setStats({
            currentLevel,
            xpToNextLevel,
            completionRate,
            totalExercises: 81,
            averageXP: user.exercises_completed ?
                Math.round(user.total_xp / user.exercises_completed) : 0
        })
    }

    useEffect(() => {
        if (user) loadUserStats()
    }, [user])

    if (loading || !user) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" text="Загрузка профиля..." />
            </div>
        )
    }

    const currentLevelXP = Math.floor(user.total_xp / 100) * 100
    const nextLevelXP = currentLevelXP + 100
    const progressPercent = ((user.total_xp - currentLevelXP) / 100) * 100

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 relative overflow-hidden">
            {/* Анимированный фон с паттерном */}
            <div className="absolute inset-0 overflow-hidden pointer-events-none">
                <div className="absolute top-0 -left-4 w-96 h-96 bg-purple-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob"></div>
                <div className="absolute top-40 -right-4 w-96 h-96 bg-blue-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-2000"></div>
                <div className="absolute -bottom-8 left-1/3 w-96 h-96 bg-pink-300 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-blob animation-delay-4000"></div>
            </div>

            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10">
                {/* Заголовок профиля */}
                <div className="mb-8 p-8 bg-gradient-to-r from-blue-100 via-purple-100 to-pink-100 rounded-3xl border-2 border-blue-200 animate-fadeIn shadow-xl">
                    <div className="flex items-center gap-6">
                        <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-5xl shadow-lg animate-pulse">
                            👤
                        </div>
                        <div>
                            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
                                {user.username}
                            </h1>
                            <p className="text-xl text-gray-700 flex items-center gap-2">
                                📧 {user.email}
                            </p>
                        </div>
                    </div>
                </div>

                {/* Основная статистика */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                    <Card className="text-center bg-gradient-to-br from-yellow-400 to-orange-500 text-white shadow-xl transform hover:scale-105 transition-all duration-300">
                        <div className="text-5xl mb-3">⭐</div>
                        <h3 className="text-3xl font-bold mb-1">{user.total_xp}</h3>
                        <p className="text-white opacity-90 font-medium">Всего XP</p>
                    </Card>

                    <Card className="text-center bg-gradient-to-br from-blue-500 to-indigo-600 text-white shadow-xl transform hover:scale-105 transition-all duration-300">
                        <div className="text-5xl mb-3">📊</div>
                        <h3 className="text-3xl font-bold mb-1">{user.english_level || 'A1'}</h3>
                        <p className="text-white opacity-90 font-medium">Уровень</p>
                    </Card>

                    <Card className="text-center bg-gradient-to-br from-green-500 to-emerald-600 text-white shadow-xl transform hover:scale-105 transition-all duration-300">
                        <div className="text-5xl mb-3">✅</div>
                        <h3 className="text-3xl font-bold mb-1">{user.exercises_completed || 0}</h3>
                        <p className="text-white opacity-90 font-medium">Выполнено</p>
                    </Card>

                    <Card className="text-center bg-gradient-to-br from-red-500 to-pink-600 text-white shadow-xl transform hover:scale-105 transition-all duration-300">
                        <div className="text-5xl mb-3">🔥</div>
                        <h3 className="text-3xl font-bold mb-1">{user.streak_days || 0}</h3>
                        <p className="text-white opacity-90 font-medium">Дней подряд</p>
                    </Card>
                </div>

                {/* Прогресс */}
                <Card className="mb-8 bg-gradient-to-br from-white to-blue-50 shadow-xl">
                    <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4 flex items-center gap-2">
                        <span>📈</span> Прогресс до следующего уровня
                    </h2>
                    <div className="space-y-3">
                        <div className="flex justify-between text-sm font-semibold text-gray-600">
                            <span>{currentLevelXP} XP</span>
                            <span className="text-blue-600">{user.total_xp} XP</span>
                            <span>{nextLevelXP} XP</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-8 shadow-inner">
                            <div
                                className="bg-gradient-to-r from-blue-500 to-purple-600 h-8 rounded-full transition-all duration-500 shadow-lg flex items-center justify-end pr-4"
                                style={{ width: `${progressPercent}%` }}
                            >
                                <span className="text-white text-sm font-bold">{Math.round(progressPercent)}%</span>
                            </div>
                        </div>
                        <p className="text-center text-gray-700 font-semibold text-lg">
                            🎯 Ещё {nextLevelXP - user.total_xp} XP до следующего уровня!
                        </p>
                    </div>
                </Card>

                {/* Детальная статистика */}
                {stats && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <Card className="bg-gradient-to-br from-purple-50 to-pink-50 shadow-lg border-2 border-purple-100">
                            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                <span>📊</span> Детальная статистика
                            </h3>
                            <div className="space-y-4">
                                <div className="flex justify-between items-center p-3 bg-white rounded-lg">
                                    <span className="text-gray-700 font-medium">Текущий уровень</span>
                                    <span className="text-blue-600 font-bold text-lg">{stats.currentLevel}</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-white rounded-lg">
                                    <span className="text-gray-700 font-medium">XP до след. уровня</span>
                                    <span className="text-orange-600 font-bold text-lg">{stats.xpToNextLevel}</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-white rounded-lg">
                                    <span className="text-gray-700 font-medium">Процент завершения</span>
                                    <span className="text-green-600 font-bold text-lg">{stats.completionRate}%</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-white rounded-lg">
                                    <span className="text-gray-700 font-medium">Средний XP за задание</span>
                                    <span className="text-purple-600 font-bold text-lg">{stats.averageXP}</span>
                                </div>
                            </div>
                        </Card>

                        <Card className="bg-gradient-to-br from-blue-50 to-indigo-50 shadow-lg border-2 border-blue-100">
                            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                                <span>🎯</span> Ваши цели
                            </h3>
                            <div className="space-y-4">
                                <div className="p-4 bg-white rounded-lg border-l-4 border-blue-500">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="font-bold text-gray-800">Ежедневная практика</span>
                                        <span className="text-blue-600 font-bold">{user.streak_days}/7</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className="bg-blue-500 h-2 rounded-full"
                                            style={{ width: `${Math.min((user.streak_days / 7) * 100, 100)}%` }}
                                        ></div>
                                    </div>
                                </div>
                                <div className="p-4 bg-white rounded-lg border-l-4 border-green-500">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="font-bold text-gray-800">Пройти все уроки A1</span>
                                        <span className="text-green-600 font-bold">{Math.min(user.exercises_completed || 0, 35)}/35</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className="bg-green-500 h-2 rounded-full"
                                            style={{ width: `${Math.min(((user.exercises_completed || 0) / 35) * 100, 100)}%` }}
                                        ></div>
                                    </div>
                                </div>
                                <div className="p-4 bg-white rounded-lg border-l-4 border-purple-500">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="font-bold text-gray-800">Набрать 500 XP</span>
                                        <span className="text-purple-600 font-bold">{user.total_xp}/500</span>
                                    </div>
                                    <div className="w-full bg-gray-200 rounded-full h-2">
                                        <div
                                            className="bg-purple-500 h-2 rounded-full"
                                            style={{ width: `${Math.min((user.total_xp / 500) * 100, 100)}%` }}
                                        ></div>
                                    </div>
                                </div>
                            </div>
                        </Card>
                    </div>
                )}

                {/* Информация об аккаунте */}
                <Card className="bg-gradient-to-br from-gray-50 to-gray-100 shadow-lg">
                    <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                        <span>ℹ️</span> Информация об аккаунте
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="p-3 bg-white rounded-lg">
                            <span className="text-sm text-gray-600">Имя пользователя</span>
                            <p className="font-bold text-gray-800">{user.username}</p>
                        </div>
                        <div className="p-3 bg-white rounded-lg">
                            <span className="text-sm text-gray-600">Email</span>
                            <p className="font-bold text-gray-800">{user.email}</p>
                        </div>
                        <div className="p-3 bg-white rounded-lg">
                            <span className="text-sm text-gray-600">Уровень английского</span>
                            <p className="font-bold text-gray-800">{user.english_level || 'A1'}</p>
                        </div>
                        <div className="p-3 bg-white rounded-lg">
                            <span className="text-sm text-gray-600">Дата регистрации</span>
                            <p className="font-bold text-gray-800">
                                {user.created_at ? new Date(user.created_at).toLocaleDateString('ru-RU') : 'Недавно'}
                            </p>
                        </div>
                    </div>
                </Card>
            </div>
        </div>
    )
}
