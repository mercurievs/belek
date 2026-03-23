import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { exerciseService } from '../services/exerciseService'
import { useAuth } from '../hooks/useAuth'
import { MultipleChoice } from '../components/exercises/MultipleChoice'
import { TypeAnswer } from '../components/exercises/TypeAnswer'
import { Translation } from '../components/exercises/Translation'
import { Button } from '../components/common/Button'
import { Spinner } from '../components/common/Spinner'
import { Alert } from '../components/common/Alert'

/**
 * Exercises - страница прохождения упражнений урока
 * 
 * Логика:
 * 1. Загрузка упражнений по ID урока
 * 2. Показ упражнений по одному (пошаговый режим)
 * 3. Проверка ответа через API
 * 4. Подсчёт правильных ответов и XP
 * 5. Финальный экран с результатами
 * 6. Обновление прогресса пользователя
 */
export const Exercises = () => {
    const { id } = useParams() // ID урока
    const navigate = useNavigate()
    const { refreshUser } = useAuth()

    const [exercises, setExercises] = useState([])
    const [currentIndex, setCurrentIndex] = useState(0)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    // Состояние текущего упражнения
    const [submitting, setSubmitting] = useState(false)
    const [result, setResult] = useState(null)

    // Статистика
    const [stats, setStats] = useState({
        correct: 0,
        total: 0,
        totalXP: 0
    })

    useEffect(() => {
        loadExercises()
    }, [id])

    /**
     * Загрузка упражнений урока
     */
    const loadExercises = async () => {
        try {
            setLoading(true)
            setError('')
            const data = await exerciseService.getExercisesByLesson(id)
            setExercises(data)
            setStats(prev => ({ ...prev, total: data.length }))
        } catch (err) {
            setError(err.response?.data?.detail || 'Ошибка загрузки упражнений')
        } finally {
            setLoading(false)
        }
    }

    /**
     * Проверка ответа пользователя
     */
    const handleSubmitAnswer = async (answer) => {
        const currentExercise = exercises[currentIndex]

        try {
            setSubmitting(true)
            setError('')

            console.log('Submitting answer:', answer, 'for exercise:', currentExercise.id)

            // Отправляем ответ на backend
            const response = await exerciseService.submitAnswer(currentExercise.id, answer)

            console.log('Received response:', response)

            // Сохраняем результат
            setResult(response)

            // Обновляем статистику
            if (response.correct) {
                setStats(prev => ({
                    ...prev,
                    correct: prev.correct + 1,
                    totalXP: prev.totalXP + (response.xp_earned || currentExercise.xp_reward || 10)
                }))
            }
        } catch (err) {
            console.error('Error submitting answer:', err)
            console.error('Error response:', err.response)
            const errorMessage = err.response?.data?.detail || err.message || 'Ошибка проверки ответа'
            setError(errorMessage)
            // Устанавливаем пустой результат чтобы кнопка не зависла
            setResult({ correct: false, explanation: errorMessage })
        } finally {
            setSubmitting(false)
        }
    }

    /**
     * Переход к следующему упражнению
     */
    const handleNext = () => {
        if (currentIndex < exercises.length - 1) {
            // Следующее упражнение
            setCurrentIndex(prev => prev + 1)
            setResult(null)
        } else {
            // Упражнения закончились - обновляем прогресс и показываем результаты
            refreshUser()
        }
    }

    /**
     * Завершение урока - возврат к списку
     */
    const handleFinish = () => {
        refreshUser()
        navigate('/lessons')
    }

    // Показываем загрузку
    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" text="Загрузка упражнений..." />
            </div>
        )
    }

    // Показываем ошибку
    if (error) {
        return (
            <div className="max-w-4xl mx-auto px-4 py-8">
                <Alert type="error" message={error} />
                <Button onClick={() => navigate(`/lessons/${id}`)} className="mt-4">
                    Вернуться к уроку
                </Button>
            </div>
        )
    }

    // Нет упражнений
    if (exercises.length === 0) {
        return (
            <div className="max-w-4xl mx-auto px-4 py-8 text-center">
                <div className="text-6xl mb-4">📝</div>
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                    Упражнений пока нет
                </h2>
                <Button onClick={() => navigate('/lessons')} className="mt-4">
                    Вернуться к урокам
                </Button>
            </div>
        )
    }

    const currentExercise = exercises[currentIndex]
    const isLastExercise = currentIndex === exercises.length - 1
    const isCompleted = currentIndex >= exercises.length

    // Финальный экран результатов
    if (isCompleted || (isLastExercise && result)) {
        return <CompletionScreen stats={stats} onFinish={handleFinish} />
    }

    // Прогресс бар
    const progress = ((currentIndex + 1) / exercises.length) * 100

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-4xl mx-auto px-4">
                {/* Прогресс бар */}
                <div className="mb-8">
                    <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-medium text-gray-700">
                            Упражнение {currentIndex + 1} из {exercises.length}
                        </span>
                        <span className="text-sm font-medium text-gray-700">
                            {Math.round(progress)}%
                        </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                        <div
                            className="bg-gradient-to-r from-blue-500 to-blue-600 h-full transition-all duration-500"
                            style={{ width: `${progress}%` }}
                        />
                    </div>
                </div>

                {/* Статистика */}
                <div className="flex justify-center gap-6 mb-8">
                    <div className="text-center">
                        <div className="text-2xl font-bold text-green-600">{stats.correct}</div>
                        <div className="text-sm text-gray-600">правильно</div>
                    </div>
                    <div className="text-center">
                        <div className="text-2xl font-bold text-yellow-600">{stats.totalXP}</div>
                        <div className="text-sm text-gray-600">XP заработано</div>
                    </div>
                </div>

                {/* Упражнение */}
                <div className="bg-white rounded-2xl shadow-lg p-8">
                    <ExerciseRenderer
                        exercise={currentExercise}
                        onSubmit={handleSubmitAnswer}
                        disabled={submitting || !!result}
                        result={result}
                    />

                    {/* Кнопка "Далее" */}
                    {result && (
                        <div className="mt-6 flex justify-center">
                            <Button
                                onClick={handleNext}
                                variant="primary"
                                className="px-8 py-3 text-lg"
                            >
                                {isLastExercise ? '🎉 Завершить урок' : 'Следующее упражнение →'}
                            </Button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

/**
 * ExerciseRenderer - рендерит компонент в зависимости от типа упражнения
 */
const ExerciseRenderer = ({ exercise, onSubmit, disabled, result }) => {
    switch (exercise.type) {
        case 'MULTIPLE_CHOICE':
            return (
                <MultipleChoice
                    exercise={exercise}
                    onSubmit={onSubmit}
                    disabled={disabled}
                    result={result}
                />
            )
        case 'TYPE_ANSWER':
            return (
                <TypeAnswer
                    exercise={exercise}
                    onSubmit={onSubmit}
                    disabled={disabled}
                    result={result}
                />
            )
        case 'TRANSLATION':
            return (
                <Translation
                    exercise={exercise}
                    onSubmit={onSubmit}
                    disabled={disabled}
                    result={result}
                />
            )
        default:
            return <div>Неизвестный тип упражнения</div>
    }
}

/**
 * CompletionScreen - финальный экран с результатами
 */
const CompletionScreen = ({ stats, onFinish }) => {
    const percentage = Math.round((stats.correct / stats.total) * 100)

    // Определяем оценку
    let grade = { emoji: '🌟', text: 'Отлично!', color: 'text-green-600' }
    if (percentage < 50) {
        grade = { emoji: '📚', text: 'Продолжайте практиковаться', color: 'text-orange-600' }
    } else if (percentage < 80) {
        grade = { emoji: '👍', text: 'Хорошая работа!', color: 'text-blue-600' }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
            <div className="max-w-2xl w-full bg-white rounded-2xl shadow-2xl p-8">
                {/* Заголовок */}
                <div className="text-center mb-8">
                    <div className="text-8xl mb-4">🎉</div>
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">
                        Урок завершён!
                    </h1>
                    <p className="text-xl text-gray-600">
                        Поздравляем с успешным выполнением
                    </p>
                </div>

                {/* Статистика */}
                <div className="grid grid-cols-3 gap-4 mb-8">
                    <div className="bg-green-50 rounded-lg p-6 text-center">
                        <div className="text-4xl font-bold text-green-600 mb-2">
                            {stats.correct}
                        </div>
                        <div className="text-sm text-gray-600">правильных ответов</div>
                    </div>
                    <div className="bg-blue-50 rounded-lg p-6 text-center">
                        <div className="text-4xl font-bold text-blue-600 mb-2">
                            {percentage}%
                        </div>
                        <div className="text-sm text-gray-600">точность</div>
                    </div>
                    <div className="bg-yellow-50 rounded-lg p-6 text-center">
                        <div className="text-4xl font-bold text-yellow-600 mb-2">
                            +{stats.totalXP}
                        </div>
                        <div className="text-sm text-gray-600">XP получено</div>
                    </div>
                </div>

                {/* Оценка */}
                <div className={`text-center mb-8 ${grade.color}`}>
                    <div className="text-6xl mb-2">{grade.emoji}</div>
                    <h2 className="text-2xl font-bold">{grade.text}</h2>
                </div>

                {/* Кнопки */}
                <div className="flex gap-4">
                    <Button
                        onClick={onFinish}
                        variant="primary"
                        className="flex-1 py-4 text-lg"
                    >
                        Вернуться к урокам
                    </Button>
                </div>
            </div>
        </div>
    )
}
