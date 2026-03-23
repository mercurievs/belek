import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { Card } from '../components/common/Card'
import { Button } from '../components/common/Button'
import { Spinner } from '../components/common/Spinner'

export function AdminPanel() {
    const navigate = useNavigate()
    const { user } = useAuth()
    const [activeTab, setActiveTab] = useState('statistics')
    const [statistics, setStatistics] = useState(null)
    const [users, setUsers] = useState([])
    const [lessons, setLessons] = useState([])
    const [exercises, setExercises] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [successMessage, setSuccessMessage] = useState('')


    useEffect(() => {
        if (!user) return
        if (user?.role !== 'ADMIN') {
            navigate('/dashboard')
            return
        }
        if (activeTab === 'statistics') loadStatistics()
        else if (activeTab === 'users') loadUsers()
        else if (activeTab === 'lessons') loadLessons()
        else if (activeTab === 'exercises') loadExercises()
    }, [user, navigate, activeTab])

    const showSuccess = (message) => {
        setSuccessMessage(message)
        setTimeout(() => setSuccessMessage(''), 3000)
    }

    const loadStatistics = async () => {
        setLoading(true)
        setError(null)
        try {
            const token = localStorage.getItem('token')
            const response = await fetch('http://localhost:8000/api/v1/admin/statistics', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка загрузки статистики')
            const data = await response.json()
            setStatistics(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const loadUsers = async () => {
        setLoading(true)
        setError(null)
        try {
            const token = localStorage.getItem('token')
            const response = await fetch('http://localhost:8000/api/v1/admin/users', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка загрузки пользователей')
            const data = await response.json()
            setUsers(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const loadLessons = async () => {
        setLoading(true)
        setError(null)
        try {
            const token = localStorage.getItem('token')
            const response = await fetch('http://localhost:8000/api/v1/admin/lessons', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка загрузки уроков')
            const data = await response.json()
            setLessons(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const loadExercises = async () => {
        setLoading(true)
        setError(null)
        try {
            const token = localStorage.getItem('token')
            const response = await fetch('http://localhost:8000/api/v1/admin/exercises', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка загрузки упражнений')
            const data = await response.json()
            setExercises(data)
        } catch (err) {
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }

    const toggleUserActive = async (userId, isActive) => {
        try {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://localhost:8000/api/v1/admin/users/${userId}/activate?is_active=${!isActive}`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка изменения статуса')
            showSuccess('Статус пользователя изменён')
            loadUsers()
        } catch (err) {
            setError(err.message)
        }
    }

    const deleteUser = async (userId) => {
        if (!confirm('Удалить пользователя?')) return
        try {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://localhost:8000/api/v1/admin/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка удаления')
            showSuccess('Пользователь удалён')
            loadUsers()
        } catch (err) {
            setError(err.message)
        }
    }

    const toggleLessonPublish = async (lessonId, isPublished) => {
        try {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://localhost:8000/api/v1/admin/lessons/${lessonId}?is_published=${!isPublished}`, {
                method: 'PATCH',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка изменения статуса')
            showSuccess('Статус урока изменён')
            loadLessons()
        } catch (err) {
            setError(err.message)
        }
    }

    const deleteLesson = async (lessonId) => {
        if (!confirm('Удалить урок и все его упражнения?')) return
        try {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://localhost:8000/api/v1/admin/lessons/${lessonId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка удаления')
            showSuccess('Урок удалён')
            loadLessons()
        } catch (err) {
            setError(err.message)
        }
    }

    const deleteExercise = async (exerciseId) => {
        if (!confirm('Удалить упражнение?')) return
        try {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://localhost:8000/api/v1/admin/exercises/${exerciseId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            if (!response.ok) throw new Error('Ошибка удаления')
            showSuccess('Упражнение удалено')
            loadExercises()
        } catch (err) {
            setError(err.message)
        }
    }

    // Показываем загрузку пока user загружается
    if (user === null || user === undefined) {
        return (
            <div className="max-w-7xl mx-auto px-4 py-8">
                <div className="text-center py-8">
                    <Spinner size="lg" />
                    <p className="mt-2 text-gray-600">Загрузка...</p>
                </div>
            </div>
        )
    }

    if (user?.role !== 'ADMIN') {
        return (
            <div className="max-w-7xl mx-auto px-4 py-8">
                <Alert variant="error">
                    У вас нет прав доступа к админ-панели. Ваша роль: {user?.role || 'не определена'}
                </Alert>
            </div>
        )
    }

    return (
        <div className="max-w-7xl mx-auto px-4 py-8">
            <h1 className="text-3xl font-bold mb-8 text-gray-900">Админ-панель</h1>

            {/* Уведомления */}
            {successMessage && (
                <Alert variant="success" className="mb-4" onClose={() => setSuccessMessage('')}>
                    {successMessage}
                </Alert>
            )}

            {error && (
                <Alert variant="error" className="mb-4" onClose={() => setError('')}>
                    {error}
                </Alert>
            )}

            {/* Табы */}
            <div className="mb-6 border-b border-gray-200">
                <nav className="-mb-px flex space-x-8">
                    <button
                        onClick={() => setActiveTab('statistics')}
                        className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'statistics'
                            ? 'border-indigo-500 text-indigo-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            }`}
                    >
                        📊 Статистика
                    </button>
                    <button
                        onClick={() => setActiveTab('users')}
                        className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'users'
                            ? 'border-indigo-500 text-indigo-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            }`}
                    >
                        👥 Пользователи
                    </button>
                    <button
                        onClick={() => setActiveTab('lessons')}
                        className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'lessons'
                            ? 'border-indigo-500 text-indigo-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            }`}
                    >
                        📚 Уроки
                    </button>
                    <button
                        onClick={() => setActiveTab('exercises')}
                        className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === 'exercises'
                            ? 'border-indigo-500 text-indigo-600'
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                            }`}
                    >
                        ✏️ Упражнения
                    </button>
                </nav>
            </div>

            {loading && (
                <div className="text-center py-8">
                    <Spinner size="lg" />
                    <p className="mt-2 text-gray-600">Загрузка...</p>
                </div>
            )}

            {/* Статистика */}
            {activeTab === 'statistics' && statistics && !loading && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <Card>
                        <h3 className="text-lg font-semibold mb-4 text-gray-900">👥 Пользователи</h3>
                        <div className="space-y-2">
                            <div className="flex justify-between">
                                <span className="text-gray-600">Всего:</span>
                                <span className="font-bold text-gray-900">{statistics.users.total}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Активные:</span>
                                <span className="font-bold text-green-600">{statistics.users.active}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Неактивные:</span>
                                <span className="font-bold text-red-600">{statistics.users.inactive}</span>
                            </div>
                        </div>
                    </Card>

                    <Card>
                        <h3 className="text-lg font-semibold mb-4 text-gray-900">📚 Уроки</h3>
                        <div className="space-y-2">
                            <div className="flex justify-between">
                                <span className="text-gray-600">Всего:</span>
                                <span className="font-bold text-gray-900">{statistics.lessons.total}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Опубликовано:</span>
                                <span className="font-bold text-green-600">{statistics.lessons.published}</span>
                            </div>
                            <div className="flex justify-between">
                                <span className="text-gray-600">Черновики:</span>
                                <span className="font-bold text-yellow-600">{statistics.lessons.draft}</span>
                            </div>
                        </div>
                    </Card>

                    <Card>
                        <h3 className="text-lg font-semibold mb-4 text-gray-900">📝 Упражнения</h3>
                        <div className="space-y-2">
                            <div className="flex justify-between">
                                <span className="text-gray-600">Всего:</span>
                                <span className="font-bold text-gray-900">{statistics.exercises.total}</span>
                            </div>
                        </div>
                    </Card>
                </div>
            )}

            {/* Пользователи */}
            {activeTab === 'users' && !loading && (
                <div className="bg-white rounded-lg shadow overflow-hidden">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Имя</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Роль</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">XP</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Действия</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {users.map(user => (
                                <tr key={user.id}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">{user.id}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">{user.email}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">{user.username}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2 py-1 text-xs rounded-full ${user.role === 'ADMIN' ? 'bg-purple-100 text-purple-800' :
                                            user.role === 'TEACHER' ? 'bg-blue-100 text-blue-800' :
                                                'bg-gray-100 text-gray-800'
                                            }`}>
                                            {user.role}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">{user.total_xp}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2 py-1 text-xs rounded-full ${user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                                            }`}>
                                            {user.is_active ? 'Активен' : 'Неактивен'}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                                        <Button
                                            onClick={() => toggleUserActive(user.id, user.is_active)}
                                            size="sm"
                                            variant={user.is_active ? "secondary" : "primary"}
                                        >
                                            {user.is_active ? 'Деактивировать' : 'Активировать'}
                                        </Button>
                                        <Button
                                            onClick={() => deleteUser(user.id)}
                                            size="sm"
                                            variant="danger"
                                        >
                                            Удалить
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Уроки */}
            {activeTab === 'lessons' && !loading && (
                <div className="bg-white rounded-lg shadow overflow-hidden">
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Название</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Уровень</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Упражнений</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Статус</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Действия</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {lessons.map(lesson => (
                                <tr key={lesson.id}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">{lesson.id}</td>
                                    <td className="px-6 py-4 text-sm">{lesson.title}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">{lesson.level}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm">{lesson.exercises_count}</td>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className={`px-2 py-1 text-xs rounded-full ${lesson.is_published ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                            }`}>
                                            {lesson.is_published ? 'Опубликован' : 'Черновик'}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm space-x-2">
                                        <Button
                                            onClick={() => toggleLessonPublish(lesson.id, lesson.is_published)}
                                            size="sm"
                                            variant={lesson.is_published ? "secondary" : "primary"}
                                        >
                                            {lesson.is_published ? 'Снять' : 'Опубликовать'}
                                        </Button>
                                        <Button
                                            onClick={() => deleteLesson(lesson.id)}
                                            size="sm"
                                            variant="danger"
                                        >
                                            Удалить
                                        </Button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}

            {/* Упражнения */}
            {activeTab === 'exercises' && !loading && (
                <Card>
                    <div className="overflow-x-auto">
                        <table className="min-w-full divide-y divide-gray-200">
                            <thead className="bg-gray-50">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Урок</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Тип</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Вопрос</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Действия</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white divide-y divide-gray-200">
                                {exercises.map(exercise => (
                                    <tr key={exercise.id}>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm">{exercise.id}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm">{exercise.lesson_id}</td>
                                        <td className="px-6 py-4 whitespace-nowrap">
                                            <span className={`px-2 py-1 text-xs rounded-full ${exercise.exercise_type === 'MULTIPLE_CHOICE' ? 'bg-blue-100 text-blue-800' :
                                                    exercise.exercise_type === 'TRANSLATION' ? 'bg-green-100 text-green-800' :
                                                        'bg-purple-100 text-purple-800'
                                                }`}>
                                                {exercise.exercise_type}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-sm max-w-md truncate">{exercise.question}</td>
                                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                                            <Button
                                                onClick={() => deleteExercise(exercise.id)}
                                                size="sm"
                                                variant="danger"
                                            >
                                                Удалить
                                            </Button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </Card>
            )}
        </div>
    )
}
