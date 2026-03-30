import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { exerciseService } from '../services/exerciseService'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { Spinner } from '../components/common/Spinner'
import { Alert } from '../components/common/Alert'

/**
 * Practice - страница практики со случайными упражнениями
 */
export const Practice = () => {
    const navigate = useNavigate()
    const [exercises, setExercises] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')
    const [selectedDifficulty, setSelectedDifficulty] = useState('ALL')
    const [language, setLanguage] = useState('ENGLISH')

    useEffect(() => {
        loadRandomExercises()
    }, [selectedDifficulty, language])

    /**
     * Загрузка случайных упражнений
     */
    const loadRandomExercises = async () => {
        try {
            setLoading(true)
            setError('')

            // Получаем все упражнения
            const allExercises = await exerciseService.getExercises(language)

            // Фильтруем по сложности
            let filtered = allExercises
            if (selectedDifficulty !== 'ALL') {
                filtered = allExercises.filter(ex => ex.difficulty === selectedDifficulty)
            }

            // Перемешиваем и берем первые 10
            const shuffled = filtered.sort(() => Math.random() - 0.5).slice(0, 10)
            setExercises(shuffled)
        } catch (err) {
            setError('Ошибка загрузки упражнений')
        } finally {
            setLoading(false)
        }
    }

    /**
     * Начать практику с выбранным упражнением
     */
    const handleStartExercise = (exercise) => {
        navigate(`/practice/${exercise.id}`)
    }

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <Spinner size="lg" text="Загрузка упражнений..." />
            </div>
        )
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-blue-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Заголовок */}
                <div className="mb-8 p-8 bg-gradient-to-r from-purple-50 via-pink-50 to-orange-50 rounded-2xl border-2 border-purple-100 animate-fadeIn">
                    <h1 className="text-5xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
                        ✏️ Практика
                    </h1>
                    <p className="text-xl text-gray-700">
                        Тренируйтесь на случайных упражнениях
                    </p>
                </div>

                {/* Выбор языка */}
                <div className="mb-6 flex gap-4">
                    <button
                        onClick={() => setLanguage('ENGLISH')}
                        className={`px-6 py-3 rounded-lg font-semibold transition-all ${language === 'ENGLISH'
                                ? 'bg-blue-600 text-white shadow-lg'
                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            }`}
                    >
                        🇬🇧 Английский
                    </button>
                    <button
                        onClick={() => setLanguage('KYRGYZ')}
                        className={`px-6 py-3 rounded-lg font-semibold transition-all ${language === 'KYRGYZ'
                                ? 'bg-red-600 text-white shadow-lg'
                                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                            }`}
                    >
                        🇰🇬 Кыргызский
                    </button>
                </div>

                {/* Фильтр по сложности */}
                <Card className="mb-6 bg-white shadow-lg">
                    <h2 className="text-xl font-bold text-gray-800 mb-4">Выберите сложность:</h2>
                    <div className="flex flex-wrap gap-3">
                        {['ALL', 'EASY', 'MEDIUM', 'HARD'].map(level => (
                            <Button
                                key={level}
                                onClick={() => setSelectedDifficulty(level)}
                                variant={selectedDifficulty === level ? 'primary' : 'secondary'}
                                className={`px-6 py-3 transform hover:scale-105 transition-all duration-300 ${selectedDifficulty === level
                                    ? 'bg-gradient-to-r from-purple-500 to-pink-600 text-white shadow-lg'
                                    : 'bg-gray-100 hover:bg-gray-200'
                                    }`}
                            >
                                {level === 'ALL' && '🎯 Все уровни'}
                                {level === 'EASY' && '🟢 Легкий'}
                                {level === 'MEDIUM' && '🟡 Средний'}
                                {level === 'HARD' && '🔴 Сложный'}
                            </Button>
                        ))}
                    </div>
                </Card>

                {/* Ошибка */}
                {error && (
                    <div className="mb-6">
                        <Alert type="error" message={error} onClose={() => setError('')} />
                    </div>
                )}

                {/* Список упражнений */}
                {exercises.length === 0 ? (
                    <Card className="text-center py-12">
                        <div className="text-6xl mb-4 animate-bounce">📝</div>
                        <h3 className="text-2xl font-bold text-gray-800 mb-2">
                            Упражнений не найдено
                        </h3>
                        <p className="text-gray-600">
                            Попробуйте выбрать другую сложность
                        </p>
                    </Card>
                ) : (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {exercises.map((exercise, index) => (
                            <div
                                key={exercise.id}
                                className="animate-slideInRight"
                                style={{ animationDelay: `${index * 0.05}s` }}
                            >
                                <Card className="bg-gradient-to-br from-white to-purple-50 hover:shadow-2xl transform hover:scale-105 transition-all duration-300 border-2 border-purple-100">
                                    {/* Тип и сложность */}
                                    <div className="flex justify-between items-start mb-4">
                                        <span className="px-3 py-1 bg-gradient-to-r from-purple-400 to-pink-500 text-white text-sm font-bold rounded-full">
                                            {exercise.type === 'MULTIPLE_CHOICE' && '📝 Выбор'}
                                            {exercise.type === 'TYPE_ANSWER' && '⌨️ Ввод'}
                                            {exercise.type === 'TRANSLATION' && '🌍 Перевод'}
                                        </span>
                                        <span className={`px-3 py-1 text-sm font-bold rounded-full ${exercise.difficulty === 'EASY' ? 'bg-green-100 text-green-700' :
                                            exercise.difficulty === 'MEDIUM' ? 'bg-yellow-100 text-yellow-700' :
                                                'bg-red-100 text-red-700'
                                            }`}>
                                            {exercise.difficulty === 'EASY' && '🟢 Легкий'}
                                            {exercise.difficulty === 'MEDIUM' && '🟡 Средний'}
                                            {exercise.difficulty === 'HARD' && '🔴 Сложный'}
                                        </span>
                                    </div>

                                    {/* Вопрос */}
                                    <h3 className="text-lg font-bold text-gray-800 mb-4 line-clamp-2">
                                        {exercise.question}
                                    </h3>

                                    {/* Награда и кнопка */}
                                    <div className="flex justify-between items-center pt-4 border-t-2 border-purple-100">
                                        <div className="flex items-center text-amber-600 font-bold">
                                            <span className="text-2xl mr-2">⭐</span>
                                            <span>+{exercise.xp_reward} XP</span>
                                        </div>
                                        <Button
                                            onClick={() => handleStartExercise(exercise)}
                                            className="bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700 text-white px-6 py-2 transform hover:scale-105 transition-all duration-300 shadow-md"
                                        >
                                            Начать 🚀
                                        </Button>
                                    </div>
                                </Card>
                            </div>
                        ))}
                    </div>
                )}

                {/* Кнопка обновить */}
                {exercises.length > 0 && (
                    <div className="mt-8 text-center">
                        <Button
                            onClick={loadRandomExercises}
                            className="bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white px-8 py-4 text-lg transform hover:scale-105 transition-all duration-300 shadow-lg"
                        >
                            🔄 Обновить упражнения
                        </Button>
                    </div>
                )}
            </div>
        </div>
    )
}
