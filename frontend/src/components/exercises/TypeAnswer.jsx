import { useState } from 'react'
import { Button } from '../common/Button'
import { Input } from '../common/Input'

/**
 * TypeAnswer - компонент упражнения с вводом ответа вручную
 * 
 * Пропсы:
 * - exercise: объект упражнения { question, correct_answer }
 * - onSubmit: функция отправки ответа (answer) => void
 * - disabled: блокировка после отправки
 * - result: результат проверки { correct, explanation }
 */
export const TypeAnswer = ({ exercise, onSubmit, disabled, result }) => {
    const [answer, setAnswer] = useState('')

    /**
     * Отправка ответа
     */
    const handleSubmit = (e) => {
        e.preventDefault()
        if (answer.trim() && onSubmit) {
            onSubmit(answer.trim())
        }
    }

    return (
        <div className="w-full max-w-2xl mx-auto">
            {/* Вопрос */}
            <div className="mb-8 p-6 bg-gradient-to-r from-cyan-50 to-blue-50 rounded-xl border-2 border-cyan-100 animate-fadeIn">
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                    {exercise.question}
                </h2>
                {exercise.context && (
                    <p className="text-gray-600 italic">
                        {exercise.context}
                    </p>
                )}
            </div>

            {/* Форма ввода */}
            <form onSubmit={handleSubmit} className="mb-6 animate-slideInRight">
                <div className="relative">
                    <Input
                        type="text"
                        value={answer}
                        onChange={(e) => setAnswer(e.target.value)}
                        placeholder="Введите ваш ответ..."
                        disabled={disabled}
                        className="text-lg p-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300"
                    />
                    {answer && !disabled && (
                        <span className="absolute right-4 top-1/2 transform -translate-y-1/2 text-2xl animate-pulse">
                            ✍️
                        </span>
                    )}
                </div>

                {/* Подсказка */}
                <div className="mt-3 p-3 bg-gradient-to-r from-amber-50 to-yellow-50 rounded-lg border border-amber-200">
                    <p className="text-sm text-amber-800 flex items-center">
                        <span className="text-lg mr-2">💡</span>
                        Совет: проверьте правописание перед отправкой
                    </p>
                </div>

                {/* Кнопка отправки */}
                {!result && (
                    <Button
                        type="submit"
                        disabled={!answer.trim() || disabled}
                        variant="primary"
                        className="w-full py-4 text-lg mt-4 bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
                    >
                        Проверить ответ
                    </Button>
                )}
            </form>

            {/* Результат */}
            {result && (
                <div className={`
          p-6 rounded-xl animate-scaleIn shadow-lg
          ${result.correct ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400' : 'bg-gradient-to-r from-red-50 to-pink-50 border-2 border-red-400'}
        `}>
                    <div className="flex items-start">
                        <span className={`text-4xl mr-4 ${result.correct ? 'animate-bounce' : ''}`}>
                            {result.correct ? '🎉' : '💡'}
                        </span>
                        <div className="flex-1">
                            <h3 className={`font-bold text-xl mb-2 ${result.correct ? 'text-green-800' : 'text-red-800'}`}>
                                {result.correct ? 'Отлично! Правильный ответ!' : 'Не совсем верно'}
                            </h3>

                            {/* Правильный ответ */}
                            {!result.correct && (
                                <div className="mt-3 p-3 bg-white/50 rounded-lg border border-gray-200">
                                    <p className="text-sm text-gray-600 mb-1">Правильный ответ:</p>
                                    <p className="font-bold text-lg text-gray-900">{exercise.correct_answer}</p>
                                </div>
                            )}

                            {/* Объяснение */}
                            {result.explanation && (
                                <p className="text-gray-700 mt-3 leading-relaxed">{result.explanation}</p>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
