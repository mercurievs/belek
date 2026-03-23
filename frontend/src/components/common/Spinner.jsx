/**
 * Spinner - индикатор загрузки
 * 
 * Пропсы:
 * - size: 'sm' | 'md' | 'lg'
 * - text: текст под спиннером
 */
export const Spinner = ({ size = 'md', text = '' }) => {
    const sizes = {
        sm: 'h-8 w-8',
        md: 'h-12 w-12',
        lg: 'h-16 w-16'
    }

    return (
        <div className="flex flex-col items-center justify-center">
            <div
                className={`
          animate-spin rounded-full 
          border-b-2 border-blue-600
          ${sizes[size]}
        `}
            />
            {text && (
                <p className="mt-4 text-gray-600">{text}</p>
            )}
        </div>
    )
}

/**
 * FullPageSpinner - загрузка на всю страницу
 */
export const FullPageSpinner = ({ text = 'Загрузка...' }) => {
    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <Spinner size="lg" text={text} />
        </div>
    )
}
