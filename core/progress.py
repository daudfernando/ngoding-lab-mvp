from datetime import datetime

from sqlalchemy import and_, func

from core.models import Enrollment, Lesson, StudentProgress, Task


def get_student_courses(db, user_id: int):
    return (
        db.query(Enrollment)
        .join(Enrollment.course)
        .filter(
            Enrollment.user_id == user_id,
            Enrollment.status == "active",
            Enrollment.course.has(is_active=True),
        )
        .all()
    )


def completed_task_ids(db, user_id: int):
    rows = db.query(StudentProgress.task_id).filter(
        StudentProgress.user_id == user_id,
        StudentProgress.is_completed.is_(True),
    )
    return {row[0] for row in rows}


def mark_task_completed(db, user_id: int, course_id: int, lesson_id: int, task_id: int) -> None:
    progress = (
        db.query(StudentProgress)
        .filter(
            StudentProgress.user_id == user_id,
            StudentProgress.task_id == task_id,
            StudentProgress.is_completed.is_(True),
        )
        .first()
    )
    if not progress:
        db.add(
            StudentProgress(
                user_id=user_id,
                course_id=course_id,
                lesson_id=lesson_id,
                task_id=task_id,
                is_completed=True,
                completed_at=datetime.utcnow(),
            )
        )
        db.commit()


def lesson_is_completed(db, user_id: int, lesson_id: int) -> bool:
    total = db.query(Task).filter(Task.lesson_id == lesson_id, Task.is_active.is_(True)).count()
    if total == 0:
        return True
    done = (
        db.query(StudentProgress)
        .filter(
            StudentProgress.user_id == user_id,
            StudentProgress.lesson_id == lesson_id,
            StudentProgress.is_completed.is_(True),
        )
        .count()
    )
    return done >= total


def unlocked_lesson_ids(db, user_id: int, course_id: int):
    lessons = (
        db.query(Lesson)
        .filter(Lesson.course_id == course_id, Lesson.is_active.is_(True))
        .order_by(Lesson.lesson_order.asc(), Lesson.id.asc())
        .all()
    )
    unlocked = set()
    previous_done = True
    for lesson in lessons:
        if previous_done:
            unlocked.add(lesson.id)
        previous_done = lesson_is_completed(db, user_id, lesson.id)
    return unlocked


def course_progress(db, user_id: int, course_id: int):
    total = (
        db.query(Task)
        .join(Lesson)
        .filter(Lesson.course_id == course_id, Lesson.is_active.is_(True), Task.is_active.is_(True))
        .count()
    )
    done = (
        db.query(StudentProgress)
        .filter(
            StudentProgress.user_id == user_id,
            StudentProgress.course_id == course_id,
            StudentProgress.is_completed.is_(True),
        )
        .count()
    )
    percent = int((done / total) * 100) if total else 0
    return done, total, percent
