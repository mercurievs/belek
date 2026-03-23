"""
Admin endpoints
Эндпоинты для администраторов
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.infrastructure.database.base import get_db
from app.api.deps import get_current_user
from app.infrastructure.database.models import UserModel, LessonModel, ExerciseModel
from app.domain.enums import UserRole, ExerciseType, DifficultyLevel


router = APIRouter()


def require_admin(current_user: dict = Depends(get_current_user)):
    """Проверка прав администратора"""
    if current_user.get("role") != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа"
        )
    return current_user


# ============ УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ ============

@router.get("/users")
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Получить список всех пользователей"""
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return [{
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role,
        "level": user.level,
        "total_xp": user.total_xp,
        "streak_days": user.streak_days,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "last_login": user.last_login.isoformat() if user.last_login else None
    } for user in users]


@router.patch("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role: UserRole,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Изменить роль пользователя"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user.role = role.value
    db.commit()
    db.refresh(user)
    
    return {"message": "Роль обновлена", "user_id": user_id, "new_role": role.value}


@router.patch("/users/{user_id}/activate")
def toggle_user_active(
    user_id: int,
    is_active: bool,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Активировать/деактивировать пользователя"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    user.is_active = is_active
    db.commit()
    
    return {"message": "Статус обновлён", "user_id": user_id, "is_active": is_active}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Удалить пользователя"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    db.delete(user)
    db.commit()
    
    return {"message": "Пользователь удалён", "user_id": user_id}


# ============ УПРАВЛЕНИЕ УРОКАМИ ============

@router.get("/lessons")
def get_all_lessons_admin(
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Получить все уроки (включая неопубликованные)"""
    lessons = db.query(LessonModel).all()
    return [{
        "id": lesson.id,
        "title": lesson.title,
        "description": lesson.description,
        "level": lesson.level,
        "order": lesson.order,
        "xp_reward": lesson.xp_reward,
        "is_published": lesson.is_published,
        "exercises_count": len(lesson.exercises) if lesson.exercises else 0,
        "created_at": lesson.created_at.isoformat() if lesson.created_at else None
    } for lesson in lessons]


@router.post("/lessons")
def create_lesson(
    title: str,
    description: str,
    content: str,
    level: str,
    order: int,
    xp_reward: int = 100,
    is_published: bool = False,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Создать новый урок"""
    lesson = LessonModel(
        title=title,
        description=description,
        content=content,
        level=level,
        order=order,
        xp_reward=xp_reward,
        is_published=is_published
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    
    return {"message": "Урок создан", "lesson_id": lesson.id}


@router.patch("/lessons/{lesson_id}")
def update_lesson(
    lesson_id: int,
    title: str = None,
    description: str = None,
    content: str = None,
    level: str = None,
    order: int = None,
    xp_reward: int = None,
    is_published: bool = None,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Обновить урок"""
    lesson = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    
    if title is not None:
        lesson.title = title
    if description is not None:
        lesson.description = description
    if content is not None:
        lesson.content = content
    if level is not None:
        lesson.level = level
    if order is not None:
        lesson.order = order
    if xp_reward is not None:
        lesson.xp_reward = xp_reward
    if is_published is not None:
        lesson.is_published = is_published
    
    db.commit()
    db.refresh(lesson)
    
    return {"message": "Урок обновлён", "lesson_id": lesson_id}


@router.delete("/lessons/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Удалить урок"""
    lesson = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Урок не найден")
    
    db.delete(lesson)
    db.commit()
    
    return {"message": "Урок удалён", "lesson_id": lesson_id}


# ============ УПРАВЛЕНИЕ УПРАЖНЕНИЯМИ ============

@router.get("/exercises")
def get_all_exercises_admin(
    lesson_id: int = None,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Получить все упражнения"""
    query = db.query(ExerciseModel)
    if lesson_id:
        query = query.filter(ExerciseModel.lesson_id == lesson_id)
    
    exercises = query.all()
    return [{
        "id": ex.id,
        "lesson_id": ex.lesson_id,
        "type": ex.type,
        "difficulty": ex.difficulty,
        "question": ex.question,
        "correct_answer": ex.correct_answer,
        "options": ex.options,
        "explanation": ex.explanation,
        "xp_reward": ex.xp_reward,
        "order": ex.order
    } for ex in exercises]


@router.post("/exercises")
def create_exercise(
    lesson_id: int,
    type: ExerciseType,
    difficulty: DifficultyLevel,
    question: str,
    correct_answer: str,
    options: str = None,
    explanation: str = None,
    xp_reward: int = 10,
    order: int = 0,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Создать новое упражнение"""
    exercise = ExerciseModel(
        lesson_id=lesson_id,
        type=type.value,
        difficulty=difficulty.value,
        question=question,
        correct_answer=correct_answer,
        options=options,
        explanation=explanation,
        xp_reward=xp_reward,
        order=order
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    
    return {"message": "Упражнение создано", "exercise_id": exercise.id}


@router.patch("/exercises/{exercise_id}")
def update_exercise(
    exercise_id: int,
    question: str = None,
    correct_answer: str = None,
    options: str = None,
    explanation: str = None,
    xp_reward: int = None,
    order: int = None,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Обновить упражнение"""
    exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    
    if question is not None:
        exercise.question = question
    if correct_answer is not None:
        exercise.correct_answer = correct_answer
    if options is not None:
        exercise.options = options
    if explanation is not None:
        exercise.explanation = explanation
    if xp_reward is not None:
        exercise.xp_reward = xp_reward
    if order is not None:
        exercise.order = order
    
    db.commit()
    db.refresh(exercise)
    
    return {"message": "Упражнение обновлено", "exercise_id": exercise_id}


@router.delete("/exercises/{exercise_id}")
def delete_exercise(
    exercise_id: int,
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Удалить упражнение"""
    exercise = db.query(ExerciseModel).filter(ExerciseModel.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Упражнение не найдено")
    
    db.delete(exercise)
    db.commit()
    
    return {"message": "Упражнение удалено", "exercise_id": exercise_id}


# ============ СТАТИСТИКА ============

@router.get("/statistics")
def get_statistics(
    current_user: dict = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Получить общую статистику платформы"""
    total_users = db.query(UserModel).count()
    active_users = db.query(UserModel).filter(UserModel.is_active == True).count()
    total_lessons = db.query(LessonModel).count()
    published_lessons = db.query(LessonModel).filter(LessonModel.is_published == True).count()
    total_exercises = db.query(ExerciseModel).count()
    
    return {
        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": total_users - active_users
        },
        "lessons": {
            "total": total_lessons,
            "published": published_lessons,
            "draft": total_lessons - published_lessons
        },
        "exercises": {
            "total": total_exercises
        }
    }
