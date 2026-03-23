import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { lessonService } from '../services/lessonService'
import { exerciseService } from '../services/exerciseService'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { Spinner } from '../components/common/Spinner'
import { Alert } from '../components/common/Alert'

/**
 * Lesson - страница детальной информации об уроке
 * 
 * Функции:
 * - Загрузка деталей урока по ID
 * - Показ информации: название, описание, уровень
 * - Загрузка списка упражнений
 * - Кнопка начала урока → переход к упражнениям
 */
export const Lesson = () => {
    const { id } = useParams()
    const navigate = useNavigate()

    const [lesson, setLesson] = useState(null)
    const [exercises, setExercises] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        loadLessonData()
    }, [id])

    /**
     * Загрузка данных урока и упражнений
     */
    const loadLessonData = async () => {
        try {
            setLoading(true)
            setError('')

            // Параллельная загрузка урока и упражнений
            const [lessonData, exercisesData] = await Promise.all([
                lessonService.getLessonById(id),
                exerciseService.getExercisesByLesson(id)
            ])

            setLesson(lessonData)
            setExercises(exercisesData)
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка загрузки урока')
        } finally {
            setLoading(false)
        }
    }

    /**
     * Начать урок - переход к упражнениям
     */
    const handleStartLesson = () => {
        navigate(`/lessons/${id}/exercises`)
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" text="Загрузка урока..." />
            </div>
        )
    }

    if (error) {
        return (
            <div className="max-w-4xl mx-auto px-4 py-8">
                <Alert type="error" message={error} />
                <Link to="/lessons" className="mt-4 inline-block text-blue-600 hover:text-blue-700">
                    ← Вернуться к урокам
                </Link>
            </div>
        )
    }

    if (!lesson) {
        return (
            <div className="max-w-4xl mx-auto px-4 py-8">
                <Alert type="error" message="Урок не найден" />
                <Link to="/lessons" className="mt-4 inline-block text-blue-600 hover:text-blue-700">
                    ← Вернуться к урокам
                </Link>
            </div>
        )
    }

    // Градиенты для уровней
    const levelStyles = {
        A1: {
            gradient: 'from-green-400 to-emerald-500',
            bg: 'from-green-50 to-emerald-50',
            border: 'border-green-300',
            text: 'text-green-700'
        },
        A2: {
            gradient: 'from-blue-400 to-cyan-500',
            bg: 'from-blue-50 to-cyan-50',
            border: 'border-blue-300',
            text: 'text-blue-700'
        },
        B1: {
            gradient: 'from-amber-400 to-orange-500',
            bg: 'from-amber-50 to-orange-50',
            border: 'border-amber-300',
            text: 'text-amber-700'
        },
        B2: {
            gradient: 'from-orange-400 to-red-500',
            bg: 'from-orange-50 to-red-50',
            border: 'border-orange-300',
            text: 'text-orange-700'
        },
        C1: {
            gradient: 'from-red-400 to-pink-500',
            bg: 'from-red-50 to-pink-50',
            border: 'border-red-300',
            text: 'text-red-700'
        },
        C2: {
            gradient: 'from-purple-400 to-indigo-500',
            bg: 'from-purple-50 to-indigo-50',
            border: 'border-purple-300',
            text: 'text-purple-700'
        }
    }

    const style = levelStyles[lesson.level] || levelStyles.A1

    return (
        <div className="max-w-4xl mx-auto px-4 py-8">
            {/* Навигация назад */}
            <Link
                to="/lessons"
                className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-6 transition-colors font-semibold hover:translate-x-[-4px] transition-transform"
            >
                <span className="mr-2">←</span>
                Все уроки
            </Link>

            {/* Основная карточка урока */}
            <div className={`mb-6 p-8 bg-gradient-to-br ${style.bg} border-2 ${style.border} rounded-2xl shadow-xl animate-fadeIn`}>
                <div className="flex items-start justify-between mb-6">
                    <div className="flex items-center">
                        <span className="text-7xl mr-6 animate-bounce">📖</span>
                        <div>
                            <h1 className="text-4xl font-bold text-gray-800 mb-3">
                                {lesson.title}
                            </h1>
                            <span className={`inline-block px-5 py-2 rounded-full text-sm font-bold bg-gradient-to-r ${style.gradient} text-white shadow-lg`}>
                                Уровень {lesson.level}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Описание */}
                <div className="mb-6 p-5 bg-white/50 backdrop-blur rounded-xl">
                    <h2 className="text-lg font-bold text-gray-700 mb-3 flex items-center">
                        <span className="mr-2">💡</span>
                        О чём этот урок:
                    </h2>
                    <p className="text-gray-700 leading-relaxed text-lg">
                        {lesson.description}
                    </p>
                </div>

                {/* Контент урока (теория) */}
                {lesson.content && (
                    <div className="mb-6 p-6 bg-white rounded-xl border-2 border-blue-200 shadow-lg">
                        <h2 className="text-2xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                            <span>📚</span> Теоретический материал
                        </h2>
                        <div className="text-gray-700 leading-relaxed">
                            <pre className="whitespace-pre-wrap font-sans text-base">
                                {lesson.content}
                            </pre>
                        </div>
                    </div>
                )}

                {/* Статистика урока */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 py-6 my-6">
                    <div className="text-center p-4 bg-white/60 backdrop-blur rounded-xl transform hover:scale-110 transition-transform duration-300">
                        <div className="text-3xl mb-2">✏️</div>
                        <div className="text-3xl font-bold text-gray-800">{exercises.length}</div>
                        <div className="text-sm text-gray-600 font-semibold">упражнений</div>
                    </div>
                    <div className="text-center p-4 bg-white/60 backdrop-blur rounded-xl transform hover:scale-110 transition-transform duration-300">
                        <div className="text-3xl mb-2">⭐</div>
                        <div className={`text-3xl font-bold ${style.text}`}>+{lesson.xp_reward || 50}</div>
                        <div className="text-sm text-gray-600 font-semibold">XP</div>
                    </div>
                    <div className="text-center p-4 bg-white/60 backdrop-blur rounded-xl transform hover:scale-110 transition-transform duration-300">
                        <div className="text-3xl mb-2">⏱️</div>
                        <div className="text-3xl font-bold text-gray-800">~10</div>
                        <div className="text-sm text-gray-600 font-semibold">минут</div>
                    </div>
                    <div className="text-center p-4 bg-white/60 backdrop-blur rounded-xl transform hover:scale-110 transition-transform duration-300">
                        <div className="text-3xl mb-2">🎯</div>
                        <div className={`text-3xl font-bold ${style.text}`}>{lesson.level}</div>
                        <div className="text-sm text-gray-600 font-semibold">уровень</div>
                    </div>
                </div>

                {/* Кнопка начала */}
                <div className="flex justify-center">
                    <Button
                        onClick={handleStartLesson}
                        variant="primary"
                        className="text-xl px-12 py-5 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 transform hover:scale-110 transition-all duration-300 shadow-2xl hover:shadow-3xl"
                    >
                        🚀 Начать урок
                    </Button>
                </div>
            </div>

            {/* Список упражнений (превью) */}
            <div className="p-8 bg-gradient-to-br from-gray-50 to-slate-50 rounded-2xl border-2 border-gray-200 shadow-lg animate-slideInRight">
                <h2 className="text-3xl font-bold text-gray-800 mb-6 flex items-center">
                    <span className="mr-3">📝</span>
                    Упражнения в этом уроке
                </h2>
                <div className="space-y-3">
                    {exercises.map((exercise, index) => (
                        <div key={exercise.id} className="animate-slideInRight" style={{ animationDelay: `${index * 0.1}s` }}>
                            <ExercisePreview
                                exercise={exercise}
                                index={index}
                            />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

/**
 * ExercisePreview - превью упражнения
 */
const ExercisePreview = ({ exercise, index }) => {
    // Иконки и стили для типов упражнений
    const typeConfig = {
        MULTIPLE_CHOICE: {
            icon: '📝',
            name: 'Выбор варианта',
            gradient: 'from-blue-400 to-indigo-500',
            bg: 'from-blue-50 to-indigo-50'
        },
        TYPE_ANSWER: {
            icon: '⌨️',
            name: 'Ввод ответа',
            gradient: 'from-cyan-400 to-blue-500',
            bg: 'from-cyan-50 to-blue-50'
        },
        TRANSLATION: {
            icon: '🌍',
            name: 'Перевод',
            gradient: 'from-purple-400 to-pink-500',
            bg: 'from-purple-50 to-pink-50'
        }
    }

    const config = typeConfig[exercise.type] || typeConfig.MULTIPLE_CHOICE

    return (
        <div className={`flex items-center p-5 bg-gradient-to-r ${config.bg} rounded-xl border-2 border-gray-200 hover:border-blue-300 hover:shadow-lg transform hover:-translate-y-1 transition-all duration-300`}>
            <div className={`flex items-center justify-center w-12 h-12 rounded-full bg-gradient-to-r ${config.gradient} text-white font-bold mr-5 shadow-md`}>
                {index + 1}
            </div>
            <div className="flex-1">
                <div className="flex items-center mb-2">
                    <span className="text-2xl mr-2">{config.icon}</span>
                    <span className="text-sm font-semibold text-gray-600 uppercase tracking-wide">{config.name}</span>
                </div>
                <p className="text-gray-800 font-semibold line-clamp-1">
                    {exercise.question}
                </p>
            </div>
            <div className="text-right">
                <div className="text-sm text-gray-500 mb-1">Награда</div>
                <div className="text-lg font-bold text-amber-600">+{exercise.xp_reward} XP</div>
            </div>
        </div>
    )
}
