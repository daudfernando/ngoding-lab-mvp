import streamlit as st

from core.auth import require_role, logout_user
from core.database import get_db
from core.models import Lesson, StudentProgress, Task
from core.progress import course_progress, get_student_courses, lesson_is_completed, unlocked_lesson_ids
from core.ui import apply_theme, badge, course_card, lesson_card, sidebar_user


st.set_page_config(page_title="Dashboard Siswa", layout="wide")
apply_theme()
user = require_role("student")
sidebar_user()
if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()

st.title("Dashboard Siswa")
db = get_db()
try:
    enrollments = get_student_courses(db, user["id"])
    if not enrollments:
        st.warning("Belum ada course aktif untuk akunmu.")
        st.stop()

    st.subheader("Course Kamu")
    cols = st.columns(2)
    for idx, enrollment in enumerate(enrollments):
        course = enrollment.course
        done, total, percent = course_progress(db, user["id"], course.id)
        with cols[idx % 2]:
            course_card(course.title, course.description, course.level_name, percent)
            st.progress(percent)
            if st.button("Masuk Course", key=f"course_{course.id}"):
                st.session_state["selected_course_id"] = course.id
                st.rerun()

    course_id = st.session_state.get("selected_course_id") or enrollments[0].course_id
    course = next((e.course for e in enrollments if e.course_id == course_id), enrollments[0].course)
    st.session_state["selected_course_id"] = course.id

    st.subheader(f"Course Map: {course.title}")
    lessons = (
        db.query(Lesson)
        .filter(Lesson.course_id == course.id, Lesson.is_active.is_(True))
        .order_by(Lesson.lesson_order.asc(), Lesson.id.asc())
        .all()
    )
    unlocked = unlocked_lesson_ids(db, user["id"], course.id)
    for lesson in lessons:
        total_tasks = db.query(Task).filter(Task.lesson_id == lesson.id, Task.is_active.is_(True)).count()
        done_tasks = (
            db.query(StudentProgress)
            .filter(
                StudentProgress.user_id == user["id"],
                StudentProgress.lesson_id == lesson.id,
                StudentProgress.is_completed.is_(True),
            )
            .count()
        )
        completed = lesson_is_completed(db, user["id"], lesson.id)
        if completed:
            status = "Selesai"
        elif lesson.id in unlocked:
            status = "Aktif"
        else:
            status = "Terkunci"
        lesson_card(lesson.title, lesson.description, badge(status, ""), done_tasks, total_tasks)
        disabled = lesson.id not in unlocked
        if st.button("Masuk Pertemuan", key=f"lesson_{lesson.id}", disabled=disabled):
            st.session_state["selected_lesson_id"] = lesson.id
            try:
                st.switch_page("pages/2_Lesson_Task.py")
            except Exception:
                st.info("Buka halaman Latihan dari sidebar.")
finally:
    db.close()
