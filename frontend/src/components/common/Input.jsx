/**
 * Input - переиспользуемый компонент поля ввода
 * 
 * Пропсы:
 * - label: подпись над полем
 * - type: тип input (text, email, password и т.д.)
 * - value: значение
 * - onChange: функция изменения
 * - placeholder: плейсхолдер
 * - error: текст ошибки
 * - required: обязательное ли поле
 */
export const Input = ({
    label,
    type = 'text',
    value,
    onChange,
    placeholder = '',
    error = '',
    required = false,
    ...props
}) => {
    return (
        <div className="w-full">
            {/* Подпись */}
            {label && (
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    {label}
                    {required && <span className="text-red-500 ml-1">*</span>}
                </label>
            )}

            {/* Поле ввода */}
            <input
                type={type}
                value={value}
                onChange={onChange}
                placeholder={placeholder}
                required={required}
                className={`
          w-full px-4 py-3 rounded-lg border
          focus:outline-none focus:ring-2 
          transition-all duration-200
          ${error
                        ? 'border-red-500 focus:ring-red-500'
                        : 'border-gray-300 focus:ring-blue-500'
                    }
        `}
                {...props}
            />

            {/* Сообщение об ошибке */}
            {error && (
                <p className="mt-1 text-sm text-red-600">{error}</p>
            )}
        </div>
    )
}
