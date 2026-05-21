import pandas as pd
import streamlit as st

from core.auth import logout_user, require_role
from core.database import get_db
from core.models import Course, Lesson, Task, TaskOption, TestCase
from core.ui import apply_theme, sidebar_user


st.set_page_config(page_title="Admin Lessons Tasks", layout="wide")
apply_theme()
require_role("admin")
sidebar_user()
if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()

st.title("Admin Lessons & Tasks")
db = get_db()
try:
    courses = db.query(Course).order_by(Course.title.asc()).all()
    course_map = {course.title: course for course in courses}

    st.subheader("Buat Lesson/Pertemuan")
    with st.form("create_lesson"):
        course_title = st.selectbox("Pilih course", list(course_map.keys()) or ["Belum ada course"])
        lesson_title = st.text_input("Title")
        lesson_description = st.text_area("Description")
        lesson_order = st.number_input("Lesson order", min_value=1, value=1, step=1)
        lesson_active = st.checkbox("Aktif", value=True)
        lesson_submit = st.form_submit_button("Buat Lesson")
    if lesson_submit:
        if not course_map:
            st.error("Buat course terlebih dahulu.")
        elif not lesson_title.strip():
            st.error("Title wajib diisi.")
        else:
            db.add(
                Lesson(
                    course_id=course_map[course_title].id,
                    title=lesson_title.strip(),
                    description=lesson_description.strip(),
                    lesson_order=lesson_order,
                    is_active=lesson_active,
                )
            )
            db.commit()
            st.success("Lesson berhasil dibuat.")
            st.rerun()

    st.subheader("Daftar Lesson")
    lessons = db.query(Lesson).join(Course).order_by(Course.title.asc(), Lesson.lesson_order.asc()).all()
    lesson_rows = [
        {
            "course": lesson.course.title,
            "lesson_order": lesson.lesson_order,
            "title": lesson.title,
            "jumlah task": db.query(Task).filter(Task.lesson_id == lesson.id).count(),
            "status aktif": "Aktif" if lesson.is_active else "Nonaktif",
        }
        for lesson in lessons
    ]
    st.dataframe(pd.DataFrame(lesson_rows), use_container_width=True, hide_index=True)

    st.subheader("Buat Task/Soal")
    lesson_map = {f"{lesson.course.title} - {lesson.lesson_order}. {lesson.title}": lesson for lesson in lessons}
    with st.form("create_task"):
        lesson_label = st.selectbox("Pilih lesson", list(lesson_map.keys()) or ["Belum ada lesson"])
        task_title = st.text_input("Title task")
        instruction = st.text_area("Instruction")
        task_type = st.selectbox("Task type", ["multiple_choice", "coding_output", "coding_function"])
        task_order = st.number_input("Task order", min_value=1, value=1, step=1)
        expected_answer = st.text_area("Expected answer")
        starter_code = st.text_area("Starter code", height=140)
        task_active = st.checkbox("Task aktif", value=True)
        task_submit = st.form_submit_button("Buat Task")
    if task_submit:
        if not lesson_map:
            st.error("Buat lesson terlebih dahulu.")
        elif not task_title.strip():
            st.error("Title task wajib diisi.")
        else:
            db.add(
                Task(
                    lesson_id=lesson_map[lesson_label].id,
                    title=task_title.strip(),
                    instruction=instruction.strip(),
                    task_type=task_type,
                    task_order=task_order,
                    expected_answer=expected_answer,
                    starter_code=starter_code,
                    is_active=task_active,
                )
            )
            db.commit()
            st.success("Task berhasil dibuat.")
            st.rerun()

    tasks = db.query(Task).join(Lesson).order_by(Lesson.lesson_order.asc(), Task.task_order.asc()).all()
    task_map = {f"{task.lesson.title} - {task.task_order}. {task.title} ({task.task_type})": task for task in tasks}

    st.subheader("Tambah Opsi Jawaban Multiple Choice")
    mc_tasks = {label: task for label, task in task_map.items() if task.task_type == "multiple_choice"}
    with st.form("add_option"):
        option_task_label = st.selectbox("Pilih task MC", list(mc_tasks.keys()) or ["Belum ada task multiple_choice"])
        option_text = st.text_area("Option text")
        option_correct = st.checkbox("Jawaban benar")
        option_submit = st.form_submit_button("Tambah Opsi")
    if option_submit:
        if not mc_tasks:
            st.error("Belum ada task multiple_choice.")
        elif not option_text.strip():
            st.error("Option text wajib diisi.")
        else:
            db.add(TaskOption(task_id=mc_tasks[option_task_label].id, option_text=option_text.strip(), is_correct=option_correct))
            db.commit()
            st.success("Opsi berhasil ditambahkan.")
            st.rerun()

    st.subheader("Tambah Test Case")
    code_tasks = {label: task for label, task in task_map.items() if task.task_type in ["coding_output", "coding_function"]}
    with st.form("add_test_case"):
        tc_task_label = st.selectbox("Pilih task coding", list(code_tasks.keys()) or ["Belum ada task coding"])
        input_data = st.text_area("Input data")
        expected_output = st.text_area("Expected output")
        test_order = st.number_input("Test order", min_value=1, value=1, step=1)
        tc_submit = st.form_submit_button("Tambah Test Case")
    if tc_submit:
        if not code_tasks:
            st.error("Belum ada task coding.")
        else:
            db.add(TestCase(task_id=code_tasks[tc_task_label].id, input_data=input_data, expected_output=expected_output, test_order=test_order))
            db.commit()
            st.success("Test case berhasil ditambahkan.")
            st.rerun()

    st.subheader("Daftar Task")
    task_rows = [
        {
            "lesson": task.lesson.title,
            "task_order": task.task_order,
            "title": task.title,
            "task_type": task.task_type,
            "status aktif": "Aktif" if task.is_active else "Nonaktif",
        }
        for task in tasks
    ]
    st.dataframe(pd.DataFrame(task_rows), use_container_width=True, hide_index=True)
finally:
    db.close()
