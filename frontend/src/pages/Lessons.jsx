import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { lessonService } from '../services/lessonService'
import { Card } from '../components/common/Card'
import { Spinner } from '../components/common/Spinner'
import { Alert } from '../components/common/Alert'

/**
 * Lessons - страница со списком всех уроков
 * 
 * Функции:
 * - Загружает список уроков с backend
 * - Отображает карточки уроков с информацией
 * - Фильтрация по уровню (будущая функция)
 * - Переход к деталям урока
 */
export const Lessons = () => {
    const [lessons, setLessons] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    // Загрузка уроков при монтировании компонента
    useEffect(() => {
        loadLessons()
    }, [])

    /**
     * Загрузка списка уроков
     */
    const loadLessons = async () => {
        try {
            setLoading(true)
            setError('')

            const data = await lessonService.getLessons()
            setLessons(data)
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка загрузки уроков')
        } finally {
            setLoading(false)
        }
    }

    // Показываем спиннер во время загрузки
    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" text="Загрузка уроков..." />
            </div>
        )
    }

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            {/* Заголовок */}
            <div className="mb-8 p-8 bg-gradient-to-r from-purple-50 via-pink-50 to-blue-50 rounded-2xl border-2 border-purple-100 animate-fadeIn">
                <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-2">
                    📚 Все уроки
                </h1>
                <p className="text-xl text-gray-700">
                    Выберите урок для изучения английского языка
                </p>
            </div>

            {/* Ошибка */}
            {error && (
                <div className="mb-6">
                    <Alert type="error" message={error} onClose={() => setError('')} />
                </div>
            )}

            {/* Список уроков */}
            {lessons.length === 0 ? (
                <Card>
                    <div className="text-center py-12">
                        <div className="text-6xl mb-4 animate-bounce">📖</div>
                        <h3 className="text-2xl font-bold text-gray-800 mb-2">
                            Уроков пока нет
                        </h3>
                        <p className="text-gray-600">
                            Скоро здесь появятся новые уроки
                        </p>
                    </div>
                </Card>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {lessons.map((lesson, index) => (
                        <div
                            key={lesson.id}
                            className="animate-slideInRight"
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            <LessonCard lesson={lesson} />
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}

/**
 * LessonCard - карточка урока
 */
const LessonCard = ({ lesson }) => {
    // Градиенты для разных уровней
    const levelStyles = {
        A1: {
            gradient: 'from-green-400 to-emerald-500',
            bg: 'from-green-50 to-emerald-50',
            border: 'border-green-200',
            text: 'text-green-700'
        },
        A2: {
            gradient: 'from-blue-400 to-cyan-500',
            bg: 'from-blue-50 to-cyan-50',
            border: 'border-blue-200',
            text: 'text-blue-700'
        },
        B1: {
            gradient: 'from-amber-400 to-orange-500',
            bg: 'from-amber-50 to-orange-50',
            border: 'border-amber-200',
            text: 'text-amber-700'
        },
        B2: {
            gradient: 'from-orange-400 to-red-500',
            bg: 'from-orange-50 to-red-50',
            border: 'border-orange-200',
            text: 'text-orange-700'
        },
        C1: {
            gradient: 'from-red-400 to-pink-500',
            bg: 'from-red-50 to-pink-50',
            border: 'border-red-200',
            text: 'text-red-700'
        },
        C2: {
            gradient: 'from-purple-400 to-indigo-500',
            bg: 'from-purple-50 to-indigo-50',
            border: 'border-purple-200',
            text: 'text-purple-700'
        }
    }

    const style = levelStyles[lesson.level] || levelStyles.A1

    return (
        <Link to={`/lessons/${lesson.id}`}>
            <div className={`h-full bg-gradient-to-br ${style.bg} border-2 ${style.border} rounded-2xl p-6 transform hover:scale-105 hover:shadow-2xl transition-all duration-300 group`}>
                {/* Иконка и уровень */}
                <div className="flex justify-between items-start mb-4">
                    <div className="text-5xl group-hover:scale-110 transition-transform duration-300">📖</div>
                    <span className={`px-4 py-2 rounded-full text-sm font-bold bg-gradient-to-r ${style.gradient} text-white shadow-md`}>
                        {lesson.level}
                    </span>
                </div>

                {/* Название */}
                <h3 className="text-xl font-bold text-gray-800 mb-3 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-600 group-hover:to-blue-600 group-hover:bg-clip-text transition-all duration-300">
                    {lesson.title}
                </h3>

                {/* Описание */}
                <p className="text-gray-600 mb-4 line-clamp-2 leading-relaxed">
                    {lesson.description}
                </p>

                {/* Статистика */}
                <div className="flex items-center justify-between text-sm pt-4 border-t-2 border-gray-200">
                    <div className="flex items-center space-x-1 font-semibold text-gray-700">
                        <span className="text-lg">✏️</span>
                        <span>{lesson.exercise_count || 0} упражнений</span>
                    </div>
                    <div className="flex items-center space-x-1">
                        <span className="text-lg">⭐</span>
                        <span className={`font-bold ${style.text}`}>+{lesson.xp_reward || 50} XP</span>
                    </div>
                </div>
            </div>
        </Link>
    )
}
