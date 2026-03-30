import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Input } from '../components/common/Input'
import { Button } from '../components/common/Button'
import { Alert } from '../components/common/Alert'

/**
 * Register - страница регистрации
 * 
 * Функции:
 * - Регистрация нового пользователя
 * - Валидация формы (email, username, пароль)
 * - Проверка совпадения паролей
 * - Редирект на /dashboard после успешной регистрации
 */
export const Register = () => {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        confirmPassword: ''
    })
    const [errors, setErrors] = useState({})

    const { register, loading } = useAuth()
    const navigate = useNavigate()

    /**
     * Обновление полей формы
     */
    const handleChange = (field) => (e) => {
        setFormData(prev => ({
            ...prev,
            [field]: e.target.value
        }))
        // Очищаем ошибку при изменении поля
        if (errors[field]) {
            setErrors(prev => ({ ...prev, [field]: '' }))
        }
    }

    /**
     * Валидация формы
     */
    const validate = () => {
        const newErrors = {}

        // Email
        if (!formData.email) {
            newErrors.email = 'Email обязателен'
        } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
            newErrors.email = 'Неверный формат email'
        }

        // Username
        if (!formData.username) {
            newErrors.username = 'Имя пользователя обязательно'
        } else if (formData.username.length < 3) {
            newErrors.username = 'Минимум 3 символа'
        }

        // Password
        if (!formData.password) {
            newErrors.password = 'Пароль обязателен'
        } else if (formData.password.length < 8) {
            newErrors.password = 'Минимум 8 символов'
        }

        // Confirm password
        if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = 'Пароли не совпадают'
        }

        setErrors(newErrors)
        return Object.keys(newErrors).length === 0
    }

    /**
     * Обработка отправки формы
     */
    const handleSubmit = async (e) => {
        e.preventDefault()

        // Валидация
        if (!validate()) {
            return
        }

        // Регистрация через AuthContext
        const result = await register(
            formData.email,
            formData.username,
            formData.password
        )

        if (result.success) {
            // Успешная регистрация → редирект на dashboard
            navigate('/dashboard')
        } else {
            // Ошибка → показываем сообщение
            setErrors({ general: result.error })
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
            <div className="max-w-md w-full">
                {/* Карточка с формой */}
                <div className="bg-white rounded-2xl shadow-2xl p-8">
                    {/* Заголовок */}
                    <div className="text-center mb-8">
                        <div className="text-5xl mb-4">🎓</div>
                        <h1 className="text-3xl font-bold text-gray-800 mb-2">
                            Регистрация
                        </h1>
                        <p className="text-gray-600">
                            Начните изучать английский язык уже сегодня
                        </p>
                    </div>

                    {/* Общая ошибка */}
                    {errors.general && (
                        <div className="mb-6">
                            <Alert
                                type="error"
                                message={errors.general}
                                onClose={() => setErrors(prev => ({ ...prev, general: '' }))}
                            />
                        </div>
                    )}

                    {/* Форма */}
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <Input
                            label="Email"
                            type="email"
                            value={formData.email}
                            onChange={handleChange('email')}
                            placeholder="your@email.com"
                            error={errors.email}
                            required
                        />

                        <Input
                            label="Имя пользователя"
                            type="text"
                            value={formData.username}
                            onChange={handleChange('username')}
                            placeholder="Ваше имя"
                            error={errors.username}
                            required
                        />

                        <Input
                            label="Пароль"
                            type="password"
                            value={formData.password}
                            onChange={handleChange('password')}
                            placeholder="••••••••"
                            error={errors.password}
                            required
                        />

                        <Input
                            label="Подтвердите пароль"
                            type="password"
                            value={formData.confirmPassword}
                            onChange={handleChange('confirmPassword')}
                            placeholder="••••••••"
                            error={errors.confirmPassword}
                            required
                        />

                        <Button
                            type="submit"
                            variant="primary"
                            disabled={loading}
                            className="w-full"
                        >
                            {loading ? 'Регистрация...' : 'Зарегистрироваться'}
                        </Button>
                    </form>

                    {/* Ссылка на вход */}
                    <div className="mt-6 text-center">
                        <p className="text-gray-600">
                            Уже есть аккаунт?{' '}
                            <Link
                                to="/login"
                                className="text-blue-600 hover:text-blue-700 font-semibold"
                            >
                                Войти
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
