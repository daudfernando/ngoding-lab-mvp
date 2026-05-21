from datetime import datetime, time

import pandas as pd
import streamlit as st

from core.auth import logout_user, require_role
from core.database import get_db
from core.models import Course, CourseCode, Enrollment, Lesson
from core.ui import apply_theme, sidebar_user


st.set_page_config(page_title="Kelola Course", layout="wide")
apply_theme()
require_role("admin")
sidebar_user()
if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()

st.title("Kelola Course")
db = get_db()
try:
    st.subheader("Buat Course Baru")
    with st.form("create_course"):
        title = st.text_input("Judul course")
        description = st.text_area("Deskripsi")
        level_name = st.text_input("Level", value="Beginner")
        is_active = st.checkbox("Aktif", value=True)
        submit = st.form_submit_button("Buat Course")
    if submit:
        if not title.strip():
            st.error("Judul course wajib diisi.")
        else:
            db.add(Course(title=title.strip(), description=description.strip(), level_name=level_name.strip(), is_active=is_active))
            db.commit()
            st.success("Course berhasil dibuat.")
            st.rerun()

    st.subheader("Daftar Course")
    courses = db.query(Course).order_by(Course.created_at.desc()).all()
    rows = []
    for course in courses:
        rows.append(
            {
                "judul": course.title,
                "level": course.level_name,
                "status aktif": "Aktif" if course.is_active else "Nonaktif",
                "jumlah lesson": db.query(Lesson).filter(Lesson.course_id == course.id).count(),
                "jumlah student enrolled": db.query(Enrollment).filter(Enrollment.course_id == course.id, Enrollment.status == "active").count(),
            }
        )
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.subheader("Update Course Sederhana")
    course_map = {course.title: course for course in courses}
    if course_map:
        selected_title = st.selectbox("Pilih course", list(course_map.keys()))
        course = course_map[selected_title]
        with st.form("update_course"):
            new_title = st.text_input("Judul", value=course.title)
            new_description = st.text_area("Deskripsi", value=course.description or "")
            new_level = st.text_input("Level", value=course.level_name or "")
            new_active = st.checkbox("Aktif", value=course.is_active)
            update_submit = st.form_submit_button("Simpan Update")
        if update_submit:
            course.title = new_title.strip()
            course.description = new_description.strip()
            course.level_name = new_level.strip()
            course.is_active = new_active
            db.commit()
            st.success("Course berhasil diupdate.")
            st.rerun()
    else:
        st.info("Belum ada course.")

    st.subheader("Buat Kode Kelas")
    active_course_map = {course.title: course for course in courses}
    with st.form("create_code"):
        code_course_title = st.selectbox("Pilih course", list(active_course_map.keys()) or ["Belum ada course"])
        code = st.text_input("Kode kelas").upper()
        max_users = st.number_input("Max users", min_value=1, value=30, step=1)
        use_expiry = st.checkbox("Pakai expired_at")
        expiry_date = st.date_input("Tanggal expired") if use_expiry else None
        expiry_dt = datetime.combine(expiry_date, time.max) if expiry_date else None
        code_active = st.checkbox("Kode aktif", value=True)
        code_submit = st.form_submit_button("Buat Kode")
    if code_submit:
        normalized_code = code.strip().upper()
        if not active_course_map:
            st.error("Buat course terlebih dahulu.")
        elif not normalized_code:
            st.error("Kode kelas wajib diisi.")
        elif db.query(CourseCode).filter(CourseCode.code == normalized_code).first():
            st.error("Kode kelas harus unique.")
        else:
            db.add(
                CourseCode(
                    course_id=active_course_map[code_course_title].id,
                    code=normalized_code,
                    max_users=max_users,
                    used_count=0,
                    is_active=code_active,
                    expired_at=expiry_dt,
                )
            )
            db.commit()
            st.success("Kode kelas berhasil dibuat.")
            st.rerun()

    st.subheader("Daftar Kode Kelas")
    codes = db.query(CourseCode).order_by(CourseCode.created_at.desc()).all()
    code_rows = [
        {
            "kode": item.code,
            "course": item.course.title,
            "max_users": item.max_users,
            "used_count": item.used_count,
            "status aktif": "Aktif" if item.is_active else "Nonaktif",
            "expired_at": item.expired_at.strftime("%Y-%m-%d") if item.expired_at else "-",
        }
        for item in codes
    ]
    st.dataframe(pd.DataFrame(code_rows), use_container_width=True, hide_index=True)
finally:
    db.close()
