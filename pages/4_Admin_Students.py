import pandas as pd
import streamlit as st

from core.auth import hash_password, logout_user, require_role
from core.database import get_db
from core.models import Course, Enrollment, User
from core.ui import apply_theme, sidebar_user


st.set_page_config(page_title="Kelola Siswa", layout="wide")
apply_theme()
require_role("admin")
sidebar_user()
if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()

st.title("Kelola Siswa")
db = get_db()
try:
    courses = db.query(Course).order_by(Course.title.asc()).all()
    course_map = {course.title: course for course in courses}

    st.subheader("Tambah Siswa Baru")
    with st.form("add_student"):
        name = st.text_input("Nama siswa")
        email = st.text_input("Email siswa")
        password = st.text_input("Password awal", type="password")
        course_title = st.selectbox("Course yang diberikan", list(course_map.keys()) or ["Belum ada course"])
        is_active = st.checkbox("Aktif", value=True)
        submit = st.form_submit_button("Buat Siswa")
    if submit:
        email = email.strip().lower()
        if not course_map:
            st.error("Buat course terlebih dahulu.")
        elif db.query(User).filter(User.email == email).first():
            st.error("Email sudah terdaftar.")
        elif not name.strip() or not email or not password:
            st.error("Nama, email, dan password wajib diisi.")
        else:
            student = User(name=name.strip(), email=email, password_hash=hash_password(password), role="student", is_active=is_active)
            db.add(student)
            db.commit()
            db.refresh(student)
            db.add(Enrollment(user_id=student.id, course_id=course_map[course_title].id, status="active"))
            db.commit()
            st.success("Siswa berhasil dibuat dan di-enroll.")
            st.rerun()

    st.subheader("Daftar Siswa")
    students = db.query(User).filter(User.role == "student").order_by(User.created_at.desc()).all()
    rows = []
    for student in students:
        course_names = [en.course.title for en in student.enrollments if en.status == "active"]
        rows.append(
            {
                "nama siswa": student.name,
                "email": student.email,
                "status aktif": "Aktif" if student.is_active else "Nonaktif",
                "course yang diikuti": ", ".join(course_names) or "-",
                "tanggal dibuat": student.created_at.strftime("%Y-%m-%d %H:%M"),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.subheader("Enrollment Course Tambahan")
    student_map = {f"{s.name} ({s.email})": s for s in students}
    with st.form("add_enrollment"):
        selected_student = st.selectbox("Pilih student", list(student_map.keys()) or ["Belum ada student"])
        selected_course = st.selectbox("Pilih course", list(course_map.keys()) or ["Belum ada course"], key="enroll_course")
        enroll_submit = st.form_submit_button("Tambahkan Enrollment")
    if enroll_submit and student_map and course_map:
        student = student_map[selected_student]
        course = course_map[selected_course]
        existing = (
            db.query(Enrollment)
            .filter(Enrollment.user_id == student.id, Enrollment.course_id == course.id, Enrollment.status == "active")
            .first()
        )
        if existing:
            st.warning("Student sudah terdaftar di course tersebut.")
        else:
            db.add(Enrollment(user_id=student.id, course_id=course.id, status="active"))
            db.commit()
            st.success("Enrollment berhasil ditambahkan.")
            st.rerun()

    st.subheader("Nonaktifkan Siswa")
    active_students = {f"{s.name} ({s.email})": s for s in students if s.is_active}
    selected_deactivate = st.selectbox("Pilih siswa aktif", list(active_students.keys()) or ["Tidak ada siswa aktif"])
    if st.button("Nonaktifkan Siswa") and active_students:
        student = active_students[selected_deactivate]
        student.is_active = False
        db.commit()
        st.success("Siswa berhasil dinonaktifkan.")
        st.rerun()
finally:
    db.close()
