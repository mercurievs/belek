/**
 * Alert - компонент уведомлений
 * 
 * Пропсы:
 * - variant: 'success' | 'error' | 'warning' | 'info'
 * - children: содержимое сообщения
 * - onClose: функция закрытия (если нужна кнопка закрытия)
 */
export const Alert = ({ variant = 'info', children, onClose, className = '' }) => {
    if (!children) return null

    const styles = {
        success: 'bg-green-50 border-green-500 text-green-800',
        error: 'bg-red-50 border-red-500 text-red-800',
        warning: 'bg-yellow-50 border-yellow-500 text-yellow-800',
        info: 'bg-blue-50 border-blue-500 text-blue-800'
    }

    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    }

    return (
        <div
            className={`
        border-l-4 p-4 rounded-r-lg flex items-start justify-between
        ${styles[variant]}
        ${className}
      `}
        >
            <div className="flex items-start">
                <span className="text-xl mr-3">{icons[variant]}</span>
                <div className="text-sm font-medium">{children}</div>
            </div>

            {onClose && (
                <button
                    onClick={onClose}
                    className="ml-4 text-xl hover:opacity-70 transition-opacity"
                >
                    ×
                </button>
            )}
        </div>
    )
}
