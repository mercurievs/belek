import { useState } from 'react'
import { Button } from '../common/Button'

/**
 * MultipleChoice - компонент упражнения с выбором варианта ответа
 * 
 * Пропсы:
 * - exercise: объект упражнения { question, options, correct_answer }
 * - onSubmit: функция отправки ответа (answer) => void
 * - disabled: блокировка после отправки
 * - result: результат проверки { correct, explanation }
 */
export const MultipleChoice = ({ exercise, onSubmit, disabled, result }) => {
    const [selectedOption, setSelectedOption] = useState(null)

    /**
     * Выбор варианта ответа
     */
    const handleSelectOption = (option) => {
        if (!disabled) {
            setSelectedOption(option)
        }
    }

    /**
     * Отправка ответа
     */
    const handleSubmit = () => {
        if (selectedOption && onSubmit) {
            onSubmit(selectedOption)
        }
    }

    // Парсинг опций из JSON строки
    const options = typeof exercise.options === 'string'
        ? JSON.parse(exercise.options)
        : exercise.options || []

    return (
        <div className="w-full max-w-2xl mx-auto">
            {/* Вопрос */}
            <div className="mb-8 p-6 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl border-2 border-indigo-100 animate-fadeIn">
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                    {exercise.question}
                </h2>
                {exercise.context && (
                    <p className="text-gray-600 italic">
                        {exercise.context}
                    </p>
                )}
            </div>

            {/* Варианты ответов */}
            <div className="space-y-3 mb-6">
                {options.map((option, index) => {
                    const isSelected = selectedOption === option
                    const isCorrect = result && option === exercise.correct_answer
                    const isWrong = result && isSelected && !result.correct

                    // Определяем стили
                    let optionStyles = 'border-2 border-gray-200 bg-white hover:border-blue-400 hover:shadow-md hover:-translate-y-0.5'

                    if (disabled) {
                        if (isCorrect) {
                            optionStyles = 'border-2 border-green-400 bg-gradient-to-r from-green-50 to-emerald-50 shadow-lg transform scale-105'
                        } else if (isWrong) {
                            optionStyles = 'border-2 border-red-400 bg-gradient-to-r from-red-50 to-pink-50'
                        }
                    } else if (isSelected) {
                        optionStyles = 'border-2 border-blue-500 bg-gradient-to-r from-blue-50 to-indigo-50 shadow-md transform scale-102'
                    }

                    return (
                        <button
                            key={index}
                            onClick={() => handleSelectOption(option)}
                            disabled={disabled}
                            className={`
                w-full p-4 rounded-xl text-left font-medium
                transition-all duration-300 ease-out
                disabled:cursor-not-allowed
                animate-slideInRight
                ${optionStyles}
              `}
                            style={{ animationDelay: `${index * 0.1}s` }}
                        >
                            <div className="flex items-center">
                                {/* Буква варианта */}
                                <div className={`
                  w-10 h-10 rounded-full flex items-center justify-center
                  font-bold mr-4 transition-all duration-300 shadow-sm
                  ${isSelected ? 'bg-gradient-to-br from-blue-500 to-indigo-600 text-white scale-110' : 'bg-gradient-to-br from-gray-100 to-gray-200 text-gray-600'}
                  ${isCorrect ? 'bg-gradient-to-br from-green-500 to-emerald-600 text-white scale-110' : ''}
                  ${isWrong ? 'bg-gradient-to-br from-red-500 to-pink-600 text-white scale-110' : ''}
                `}>
                                    {String.fromCharCode(65 + index)}
                                </div>

                                {/* Текст варианта */}
                                <span className="text-gray-800 flex-1">{option}</span>

                                {/* Иконка результата */}
                                {disabled && isCorrect && (
                                    <span className="ml-auto text-2xl animate-bounce">✅</span>
                                )}
                                {disabled && isWrong && (
                                    <span className="ml-auto text-2xl">❌</span>
                                )}
                            </div>
                        </button>
                    )
                })}
            </div>

            {/* Кнопка отправки */}
            {!result && (
                <Button
                    onClick={handleSubmit}
                    disabled={!selectedOption || disabled}
                    variant="primary"
                    className="w-full py-4 text-lg bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-xl"
                >
                    Проверить ответ
                </Button>
            )}

            {/* Результат */}
            {result && (
                <div className={`
          p-6 rounded-xl mt-4 animate-scaleIn shadow-lg
          ${result.correct ? 'bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400' : 'bg-gradient-to-r from-red-50 to-pink-50 border-2 border-red-400'}
        `}>
                    <div className="flex items-start">
                        <span className={`text-4xl mr-4 ${result.correct ? 'animate-bounce' : ''}`}>
                            {result.correct ? '🎉' : '💡'}
                        </span>
                        <div>
                            <h3 className={`font-bold text-xl mb-2 ${result.correct ? 'text-green-800' : 'text-red-800'}`}>
                                {result.correct ? 'Отлично! Правильный ответ!' : 'Не совсем верно'}
                            </h3>
                            {result.explanation && (
                                <p className="text-gray-700 leading-relaxed">{result.explanation}</p>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </div>
    )
}
