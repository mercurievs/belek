import { useState } from 'react'
import { Button } from '../common/Button'
import { Input } from '../common/Input'

/**
 * Translation - компонент упражнения на перевод
 * 
 * Пропсы:
 * - exercise: объект упражнения { question, correct_answer }
 * - onSubmit: функция отправки ответа (answer) => void
 * - disabled: блокировка после отправки
 * - result: результат проверки { correct, explanation }
 */
export const Translation = ({ exercise, onSubmit, disabled, result }) => {
    const [translation, setTranslation] = useState('')

    /**
     * Отправка перевода
     */
    const handleSubmit = (e) => {
        e.preventDefault()
        if (translation.trim() && onSubmit) {
            onSubmit(translation.trim())
        }
    }

    return (
        <div className="w-full max-w-2xl mx-auto">
            {/* Заголовок */}
            <div className="text-center mb-6">
                <div className="text-5xl mb-3">🌍</div>
                <h2 className="text-xl font-semibold text-gray-700">
                    Переведите предложение
                </h2>
            </div>

            {/* Предложение для перевода */}
            <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-6 mb-6">
                <p className="text-2xl text-center font-medium text-gray-800">
                    {exercise.question}
                </p>
            </div>

            {/* Форма ввода перевода */}
            <form onSubmit={handleSubmit} className="mb-6">
                <Input
                    type="text"
                    value={translation}
                    onChange={(e) => setTranslation(e.target.value)}
                    placeholder="Ваш перевод..."
                    disabled={disabled}
                    className="text-lg"
                />

                {/* Подсказка */}
                <p className="mt-2 text-sm text-gray-500">
                    💡 Совет: переводите как можно точнее
                </p>

                {/* Кнопка отправки */}
                {!result && (
                    <Button
                        type="submit"
                        disabled={!translation.trim() || disabled}
                        variant="primary"
                        className="w-full py-4 text-lg mt-4"
                    >
                        Проверить перевод
                    </Button>
                )}
            </form>

            {/* Результат */}
            {result && (
                <div className={`
          p-4 rounded-lg
          ${result.correct ? 'bg-green-50 border-2 border-green-500' : 'bg-yellow-50 border-2 border-yellow-500'}
        `}>
                    <div className="flex items-start">
                        <span className="text-3xl mr-3">
                            {result.correct ? '🎉' : '💡'}
                        </span>
                        <div className="flex-1">
                            <h3 className={`font-bold text-lg mb-1 ${result.correct ? 'text-green-800' : 'text-yellow-800'}`}>
                                {result.correct ? 'Отличный перевод!' : 'Хороший вариант!'}
                            </h3>

                            {/* Правильный перевод */}
                            <div className="mt-2">
                                <p className="text-sm text-gray-700 mb-1">
                                    {result.correct ? 'Ваш перевод верен' : 'Рекомендуемый перевод:'}
                                </p>
                                <p className="font-semibold text-gray-900">{exercise.correct_answer}</p>
                            </div>

                            {/* Объяснение */}
                            {result.explanation && (
                                <p className="text-gray-700 mt-2 text-sm">{result.explanation}</p>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
