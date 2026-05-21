import streamlit as st

try:
    from streamlit_ace import st_ace
except Exception:
    st_ace = None

from core.auth import require_role, logout_user
from core.checker import check_coding_output, check_multiple_choice
from core.database import get_db
from core.models import Lesson, Submission, StudentProgress, Task
from core.progress import get_student_courses, mark_task_completed, unlocked_lesson_ids
from core.ui import apply_theme, sidebar_user


st.set_page_config(page_title="Latihan", layout="wide")
apply_theme()
user = require_role("student")
sidebar_user()
if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()

st.title("Latihan")
db = get_db()
try:
    enrollments = get_student_courses(db, user["id"])
    if not enrollments:
        st.warning("Belum ada course aktif.")
        st.stop()

    course_options = {e.course.title: e.course for e in enrollments}
    selected_course_title = st.selectbox(
        "Pilih Course",
        list(course_options.keys()),
        index=0,
    )
    course = course_options[selected_course_title]
    st.session_state["selected_course_id"] = course.id

    unlocked = unlocked_lesson_ids(db, user["id"], course.id)
    lessons = (
        db.query(Lesson)
        .filter(Lesson.course_id == course.id, Lesson.is_active.is_(True))
        .order_by(Lesson.lesson_order.asc(), Lesson.id.asc())
        .all()
    )
    open_lessons = [lesson for lesson in lessons if lesson.id in unlocked]
    if not open_lessons:
        st.warning("Belum ada pertemuan yang bisa dibuka.")
        st.stop()

    preferred_lesson_id = st.session_state.get("selected_lesson_id")
    lesson_titles = [lesson.title for lesson in open_lessons]
    selected_index = 0
    if preferred_lesson_id in [lesson.id for lesson in open_lessons]:
        selected_index = [lesson.id for lesson in open_lessons].index(preferred_lesson_id)
    selected_lesson_title = st.selectbox("Pilih Pertemuan", lesson_titles, index=selected_index)
    lesson = open_lessons[lesson_titles.index(selected_lesson_title)]
    st.session_state["selected_lesson_id"] = lesson.id

    tasks = (
        db.query(Task)
        .filter(Task.lesson_id == lesson.id, Task.is_active.is_(True))
        .order_by(Task.task_order.asc(), Task.id.asc())
        .all()
    )
    if not tasks:
        st.info("Pertemuan ini belum memiliki task.")
        st.stop()

    completed_ids = {
        row[0]
        for row in db.query(StudentProgress.task_id).filter(
            StudentProgress.user_id == user["id"],
            StudentProgress.lesson_id == lesson.id,
            StudentProgress.is_completed.is_(True),
        )
    }
    current_task = next((task for task in tasks if task.id not in completed_ids), None)
    if current_task is None:
        st.success("Pertemuan selesai. Silakan lanjut ke pertemuan berikutnya.")
        st.stop()

    st.subheader(current_task.title)
    st.write(current_task.instruction)

    if current_task.task_type == "multiple_choice":
        options = current_task.options
        label_to_id = {option.option_text: option.id for option in options}
        selected = st.multiselect("Pilih semua jawaban yang benar", list(label_to_id.keys()))
        if st.button("Submit Jawaban"):
            selected_ids = [label_to_id[item] for item in selected]
            correct_ids = [option.id for option in options if option.is_correct]
            is_correct = check_multiple_choice(correct_ids, selected_ids)
            status = "correct" if is_correct else "incorrect"
            feedback = "Benar. Lanjut ke soal berikutnya." if is_correct else "Jawaban belum tepat. Coba lagi."
            db.add(
                Submission(
                    user_id=user["id"],
                    task_id=current_task.id,
                    submitted_answer=", ".join(selected),
                    status=status,
                    feedback=feedback,
                )
            )
            db.commit()
            if is_correct:
                mark_task_completed(db, user["id"], course.id, lesson.id, current_task.id)
                st.success(feedback)
                st.rerun()
            else:
                st.error(feedback)

    elif current_task.task_type in ["coding_output", "coding_function"]:
        st.caption("Starter code")
        st.code(current_task.starter_code or "", language="python")
        default_code = current_task.starter_code or ""
        if st_ace:
            code = st_ace(
                value=default_code,
                language="python",
                theme="chrome",
                height=260,
                key=f"code_{current_task.id}",
                auto_update=True,
            )
            code = code if code is not None else default_code
        else:
            code = st.text_area("Kode Python", value=default_code, height=260)

        if st.button("Run / Submit"):
            cases = [
                {"input_data": case.input_data, "expected_output": case.expected_output}
                for case in current_task.test_cases
            ]
            ok, status, feedback = check_coding_output(code or "", current_task.expected_answer or "", cases)
            db.add(
                Submission(
                    user_id=user["id"],
                    task_id=current_task.id,
                    submitted_code=code or "",
                    status=status,
                    feedback=feedback,
                )
            )
            db.commit()
            if ok:
                mark_task_completed(db, user["id"], course.id, lesson.id, current_task.id)
                st.success("Benar. Lanjut ke soal berikutnya.")
                st.rerun()
            elif status == "error":
                st.error(f"Kode error: {feedback}")
            else:
                st.error(feedback)
    else:
        st.error("Tipe task belum didukung.")
finally:
    db.close()
