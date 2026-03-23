import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { exerciseService } from '../services/exerciseService'
import { MultipleChoice } from '../components/exercises/MultipleChoice'
import { TypeAnswer } from '../components/exercises/TypeAnswer'
import { Spinner } from '../components/common/Spinner'
import { Button } from '../components/common/Button'

/**
 * PracticeExercise - страница выполнения одиночного упражнения в практике
 */
export const PracticeExercise = () => {
    const { id } = useParams()
    const navigate = useNavigate()

    const [exercise, setExercise] = useState(null)
    const [loading, setLoading] = useState(true)
    const [result, setResult] = useState(null)
    const [submitted, setSubmitted] = useState(false)

    useEffect(() => {
        loadExercise()
    }, [id])

    const loadExercise = async () => {
        try {
            setLoading(true)
            const data = await exerciseService.getExerciseById(id)
            setExercise(data)
        } catch (err) {
            console.error('Ошибка загрузки упражнения:', err)
        } finally {
            setLoading(false)
        }
    }

    const handleSubmit = async (answer) => {
        try {
            setSubmitted(true)
            console.log('Submitting practice answer:', answer, 'for exercise:', id)
            const checkResult = await exerciseService.submitExercise(id, answer)
            console.log('Practice result:', checkResult)
            setResult(checkResult)
        } catch (err) {
            console.error('Ошибка отправки ответа:', err)
            console.error('Error response:', err.response)
            // Устанавливаем результат с ошибкой
            setResult({
                correct: false,
                explanation: err.response?.data?.detail || err.message || 'Ошибка проверки ответа'
            })
        }
    }

    const handleNext = () => {
        navigate('/practice')
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" text="Загрузка упражнения..." />
            </div>
        )
    }

    if (!exercise) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <p className="text-xl text-gray-600">Упражнение не найдено</p>
                    <Button onClick={() => navigate('/practice')} className="mt-4">
                        Вернуться к практике
                    </Button>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50 py-8">
            <div className="max-w-4xl mx-auto px-4">
                {/* Заголовок */}
                <div className="mb-6 flex justify-between items-center">
                    <Button
                        onClick={() => navigate('/practice')}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800"
                    >
                        ← Вернуться к практике
                    </Button>
                    <div className="text-right">
                        <span className={`px-4 py-2 rounded-full text-sm font-bold ${exercise.difficulty === 'EASY' ? 'bg-green-100 text-green-700' :
                            exercise.difficulty === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
                                'bg-red-100 text-red-700'
                            }`}>
                            {exercise.difficulty === 'EASY' && '🟢 Легкий'}
                            {exercise.difficulty === 'MEDIUM' && '🟡 Средний'}
                            {exercise.difficulty === 'HARD' && '🔴 Сложный'}
                        </span>
                    </div>
                </div>

                {/* Упражнение */}
                <div className="bg-white rounded-2xl shadow-xl p-8">
                    {exercise.type === 'MULTIPLE_CHOICE' && (
                        <MultipleChoice
                            exercise={exercise}
                            onSubmit={handleSubmit}
                            disabled={submitted}
                            result={result}
                        />
                    )}
                    {exercise.type === 'TYPE_ANSWER' && (
                        <TypeAnswer
                            exercise={exercise}
                            onSubmit={handleSubmit}
                            disabled={submitted}
                            result={result}
                        />
                    )}
                    {exercise.type === 'TRANSLATION' && (
                        <TypeAnswer
                            exercise={exercise}
                            onSubmit={handleSubmit}
                            disabled={submitted}
                            result={result}
                        />
                    )}
                </div>

                {/* Кнопка продолжить */}
                {result && (
                    <div className="mt-6 text-center">
                        <Button
                            onClick={handleNext}
                            className="bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 text-white px-8 py-4 text-lg transform hover:scale-105 transition-all duration-300 shadow-lg"
                        >
                            Продолжить практику 🚀
                        </Button>
                    </div>
                )}
            </div>
        </div>
    )
}
