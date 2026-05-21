import pandas as pd
import streamlit as st

from core.auth import logout_user, require_role
from core.database import get_db
from core.models import Course, Enrollment, Lesson, StudentProgress, Submission, Task, User
from core.ui import apply_theme, metric_card, sidebar_user


st.set_page_config(page_title="Admin Reports", layout="wide")
apply_theme()
require_role("admin")
sidebar_user()
if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()

st.title("Admin Reports")
db = get_db()
try:
    st.subheader("Ringkasan")
    cols = st.columns(6)
    metrics = [
        ("Student", db.query(User).filter(User.role == "student").count()),
        ("Course", db.query(Course).count()),
        ("Lesson", db.query(Lesson).count()),
        ("Task", db.query(Task).count()),
        ("Submission", db.query(Submission).count()),
        ("Completed Task", db.query(StudentProgress).filter(StudentProgress.is_completed.is_(True)).count()),
    ]
    for col, (label, value) in zip(cols, metrics):
        with col:
            metric_card(label, value)

    st.subheader("Progress Student")
    progress_rows = []
    enrollments = db.query(Enrollment).join(User).join(Course).filter(User.role == "student").all()
    for enrollment in enrollments:
        total_lessons = db.query(Lesson).filter(Lesson.course_id == enrollment.course_id, Lesson.is_active.is_(True)).count()
        total_tasks = (
            db.query(Task)
            .join(Lesson)
            .filter(Lesson.course_id == enrollment.course_id, Task.is_active.is_(True), Lesson.is_active.is_(True))
            .count()
        )
        done_tasks = (
            db.query(StudentProgress)
            .filter(
                StudentProgress.user_id == enrollment.user_id,
                StudentProgress.course_id == enrollment.course_id,
                StudentProgress.is_completed.is_(True),
            )
            .count()
        )
        percent = round((done_tasks / total_tasks) * 100, 2) if total_tasks else 0
        progress_rows.append(
            {
                "nama student": enrollment.user.name,
                "email": enrollment.user.email,
                "course": enrollment.course.title,
                "total lesson": total_lessons,
                "total task": total_tasks,
                "task selesai": done_tasks,
                "persentase progress": percent,
            }
        )
    progress_df = pd.DataFrame(progress_rows)
    st.dataframe(progress_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Progress Report CSV",
        progress_df.to_csv(index=False).encode("utf-8"),
        "progress_report.csv",
        "text/csv",
        disabled=progress_df.empty,
    )

    st.subheader("Submission Terbaru")
    submissions = (
        db.query(Submission)
        .join(User)
        .join(Task)
        .order_by(Submission.created_at.desc())
        .limit(100)
        .all()
    )
    submission_rows = []
    for submission in submissions:
        task = submission.task
        lesson = task.lesson
        submission_rows.append(
            {
                "nama student": submission.user.name,
                "course": lesson.course.title,
                "lesson": lesson.title,
                "task": task.title,
                "status": submission.status,
                "waktu submit": submission.created_at.strftime("%Y-%m-%d %H:%M"),
            }
        )
    submission_df = pd.DataFrame(submission_rows)
    st.dataframe(submission_df, use_container_width=True, hide_index=True)
    st.download_button(
        "Download Submission Report CSV",
        submission_df.to_csv(index=False).encode("utf-8"),
        "submission_report.csv",
        "text/csv",
        disabled=submission_df.empty,
    )
finally:
    db.close()
