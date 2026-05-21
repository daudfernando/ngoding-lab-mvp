from datetime import datetime

import streamlit as st

from core.auth import authenticate_user, current_user, login_user, logout_user
from core.auth import hash_password
from core.database import get_db, init_db
from core.models import CourseCode, Enrollment, User
from core.seed import seed_if_empty
from core.ui import apply_theme, sidebar_user


st.set_page_config(page_title="Ngoding Lab MVP", page_icon="NL", layout="wide")
apply_theme()
init_db()
db = get_db()
try:
    seed_if_empty(db)
finally:
    db.close()


def do_switch(page):
    try:
        st.switch_page(page)
    except Exception:
        st.info(f"Buka halaman `{page}` dari sidebar.")


def login_view():
    st.title("Ngoding Lab MVP")
    st.caption("Platform latihan coding untuk siswa pemula.")

    login_tab, register_tab = st.tabs(["Login", "Daftar dengan Kode Kelas"])
    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
        if submitted:
            user = authenticate_user(email, password)
            if not user:
                st.error("Email atau password salah, atau akun belum aktif.")
            else:
                login_user(user)
                st.success("Login berhasil.")
                if user.role == "admin":
                    do_switch("pages/3_Admin_Dashboard.py")
                else:
                    do_switch("pages/1_Student_Dashboard.py")
                st.rerun()

    with register_tab:
        with st.form("register_code_form"):
            name = st.text_input("Nama")
            reg_email = st.text_input("Email siswa")
            reg_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Konfirmasi password", type="password")
            code = st.text_input("Kode kelas")
            register_submit = st.form_submit_button("Daftar")
        if register_submit:
            db = get_db()
            try:
                reg_email = reg_email.strip().lower()
                code_value = code.strip().upper()
                existing = db.query(User).filter(User.email == reg_email).first()
                course_code = db.query(CourseCode).filter(CourseCode.code == code_value).first()
                if not name.strip() or not reg_email or not reg_password:
                    st.error("Nama, email, dan password wajib diisi.")
                elif existing:
                    st.error("Email sudah terdaftar.")
                elif reg_password != confirm_password:
                    st.error("Password dan konfirmasi password tidak sama.")
                elif not course_code or not course_code.is_active:
                    st.error("Kode kelas tidak aktif atau tidak ditemukan.")
                elif course_code.used_count >= course_code.max_users:
                    st.error("Kuota kode kelas sudah penuh.")
                elif course_code.expired_at and course_code.expired_at < datetime.utcnow():
                    st.error("Kode kelas sudah kedaluwarsa.")
                else:
                    user = User(
                        name=name.strip(),
                        email=reg_email,
                        password_hash=hash_password(reg_password),
                        role="student",
                        is_active=True,
                    )
                    db.add(user)
                    db.commit()
                    db.refresh(user)
                    db.add(Enrollment(user_id=user.id, course_id=course_code.course_id, status="active"))
                    course_code.used_count += 1
                    db.commit()
                    st.success("Daftar berhasil. Silakan login.")
            finally:
                db.close()


user = current_user()
if not user:
    login_view()
    st.stop()

sidebar_user()
if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()

st.title("Ngoding Lab MVP")
st.write(f"Halo, **{user['name']}**.")
if user["role"] == "admin":
    st.info("Gunakan sidebar untuk membuka Admin Dashboard, mengelola siswa, course, lesson, task, dan laporan.")
    if st.button("Buka Admin Dashboard"):
        do_switch("pages/3_Admin_Dashboard.py")
else:
    st.info("Gunakan sidebar untuk membuka Student Dashboard dan mulai mengerjakan latihan.")
    if st.button("Buka Student Dashboard"):
        do_switch("pages/1_Student_Dashboard.py")
