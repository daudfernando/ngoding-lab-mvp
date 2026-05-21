import streamlit as st

from core.auth import require_role, logout_user
from core.database import get_db
from core.models import Course, Lesson, Submission, Task, User
from core.ui import apply_theme, metric_card, sidebar_user


st.set_page_config(page_title="Dashboard Admin", layout="wide")
apply_theme()
user = require_role("admin")
sidebar_user()
if st.sidebar.button("Logout"):
    logout_user()
    st.rerun()

st.title("Dashboard Admin")
st.caption("Ringkasan cepat Ngoding Lab.")

db = get_db()
try:
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Student", db.query(User).filter(User.role == "student").count())
    with c2:
        metric_card("Course", db.query(Course).count())
    with c3:
        metric_card("Lesson", db.query(Lesson).count())
    with c4:
        metric_card("Task", db.query(Task).count())
    with c5:
        metric_card("Submission", db.query(Submission).count())
    st.info("Kelola siswa, course, pertemuan, latihan, dan laporan dari sidebar.")
finally:
    db.close()
