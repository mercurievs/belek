/**
 * Card - карточка для контента
 * 
 * Пропсы:
 * - children: содержимое карточки
 * - className: дополнительные классы
 * - hover: добавить эффект hover
 * - onClick: обработчик клика (если нужна кликабельная карточка)
 */
export const Card = ({
    children,
    className = '',
    hover = false,
    onClick
}) => {
    const baseStyles = 'bg-white rounded-xl shadow-md p-6 transition-all duration-200'
    const hoverStyles = hover ? 'hover:shadow-lg hover:scale-105 cursor-pointer' : ''

    return (
        <div
            className={`${baseStyles} ${hoverStyles} ${className}`}
            onClick={onClick}
        >
            {children}
        </div>
    )
}
