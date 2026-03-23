import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Input } from '../components/common/Input'
import { Button } from '../components/common/Button'
import { Alert } from '../components/common/Alert'

/**
 * Login - страница входа в систему
 * 
 * Функции:
 * - Вход по email и паролю
 * - Валидация формы
 * - Отображение ошибок
 * - Редирект на /dashboard после успешного входа
 */
export const Login = () => {
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')

    const { login, loading } = useAuth()
    const navigate = useNavigate()

    /**
     * Обработка отправки формы
     */
    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')

        // Простая валидация
        if (!email || !password) {
            setError('Заполните все поля')
            return
        }

        // Вход через AuthContext
        const result = await login(email, password)

        if (result.success) {
            // Успешный вход → редирект на dashboard
            navigate('/dashboard')
        } else {
            // Ошибка → показываем сообщение
            setError(result.error)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100 flex items-center justify-center p-4 relative overflow-hidden">
            {/* Анимированный фон */}
            <div className="absolute inset-0 overflow-hidden">
                <div className="absolute w-96 h-96 bg-blue-400/20 rounded-full blur-3xl -top-48 -left-48 animate-pulse"></div>
                <div className="absolute w-96 h-96 bg-purple-400/20 rounded-full blur-3xl -bottom-48 -right-48 animate-pulse" style={{ animationDelay: '1s' }}></div>
            </div>

            <div className="max-w-md w-full relative z-10">
                {/* Карточка с формой */}
                <div className="bg-white/90 backdrop-blur-lg rounded-3xl shadow-2xl p-10 border-2 border-white/50 animate-scaleIn">
                    {/* Заголовок */}
                    <div className="text-center mb-8">
                        <div className="text-6xl mb-4 animate-bounce">🎓</div>
                        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">
                            Вход в систему
                        </h1>
                        <p className="text-gray-600 text-lg">
                            Продолжите изучение английского языка
                        </p>
                    </div>

                    {/* Ошибка */}
                    {error && (
                        <div className="mb-6 animate-slideInRight">
                            <Alert type="error" message={error} onClose={() => setError('')} />
                        </div>
                    )}

                    {/* Форма */}
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="animate-slideInRight" style={{ animationDelay: '0.1s' }}>
                            <Input
                                label="Email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="your@email.com"
                                required
                                className="border-2 border-gray-200 focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all duration-300"
                            />
                        </div>

                        <div className="animate-slideInRight" style={{ animationDelay: '0.2s' }}>
                            <Input
                                label="Пароль"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                required
                                className="border-2 border-gray-200 focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all duration-300"
                            />
                        </div>

                        <div className="animate-slideInRight" style={{ animationDelay: '0.3s' }}>
                            <Button
                                type="submit"
                                variant="primary"
                                disabled={loading}
                                className="w-full text-lg py-4 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 transform hover:scale-105 transition-all duration-300 shadow-lg hover:shadow-2xl"
                            >
                                {loading ? (
                                    <span className="flex items-center justify-center">
                                        <span className="animate-spin mr-2">⏳</span>
                                        Вход...
                                    </span>
                                ) : (
                                    'Войти 🚀'
                                )}
                            </Button>
                        </div>
                    </form>

                    {/* Ссылка на регистрацию */}
                    <div className="mt-8 text-center animate-fadeIn" style={{ animationDelay: '0.4s' }}>
                        <p className="text-gray-600 text-lg">
                            Ещё нет аккаунта?{' '}
                            <Link
                                to="/register"
                                className="text-blue-600 hover:text-purple-600 font-bold transition-colors"
                            >
                                Зарегистрироваться
                            </Link>
                        </p>
                    </div>

                    {/* Тестовые данные (для демо) */}
                    <div className="mt-6 p-5 bg-gradient-to-r from-amber-50 to-yellow-50 rounded-2xl border-2 border-amber-200 animate-fadeIn" style={{ animationDelay: '0.5s' }}>
                        <p className="text-sm font-bold mb-2 flex items-center text-amber-800">
                            <span className="text-xl mr-2">🔑</span>
                            Тестовые данные:
                        </p>
                        <p className="text-sm text-amber-700 font-mono bg-white/50 p-2 rounded">
                            test@example.com / password123
                        </p>
                    </div>
                </div>
            </div>
        </div>
    )
}
