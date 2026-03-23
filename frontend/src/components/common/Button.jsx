/**
 * Button - переиспользуемый компонент кнопки
 * 
 * Пропсы:
 * - children: текст кнопки
 * - variant: 'primary' | 'secondary' | 'danger'
 * - size: 'sm' | 'md' | 'lg'
 * - disabled: boolean
 * - onClick: функция обработчик
 * - type: 'button' | 'submit'
 * - className: дополнительные классы
 */
export const Button = ({
    children,
    variant = 'primary',
    size = 'md',
    disabled = false,
    onClick,
    type = 'button',
    className = ''
}) => {
    // Базовые стили для всех кнопок
    const baseStyles = 'rounded-lg font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed'

    // Размеры
    const sizeStyles = {
        sm: 'px-3 py-1.5 text-sm',
        md: 'px-6 py-3',
        lg: 'px-8 py-4 text-lg'
    }

    // Стили в зависимости от варианта
    const variantStyles = {
        primary: 'bg-blue-600 hover:bg-blue-700 text-white',
        secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
        danger: 'bg-red-600 hover:bg-red-700 text-white',
        success: 'bg-green-600 hover:bg-green-700 text-white'
    }

    return (
        <button
            type={type}
            onClick={onClick}
            disabled={disabled}
            className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} ${className}`}
        >
            {children}
        </button>
    )
}
