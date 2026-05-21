import streamlit as st
from passlib.context import CryptContext

from core.database import get_db
from core.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return pwd_context.verify(password, password_hash)
    except Exception:
        return False


def authenticate_user(email: str, password: str):
    db = get_db()
    try:
        user = db.query(User).filter(User.email == email.strip().lower()).first()
        if not user or not user.is_active:
            return None
        if verify_password(password, user.password_hash):
            return user
        return None
    finally:
        db.close()


def login_user(user: User) -> None:
    st.session_state["user"] = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
    }


def logout_user() -> None:
    for key in ["user", "selected_course_id", "selected_lesson_id"]:
        st.session_state.pop(key, None)
    try:
        st.switch_page("app.py")
    except Exception:
        st.rerun()


def current_user():
    return st.session_state.get("user")


def require_login():
    user = current_user()
    if not user:
        st.warning("Silakan login terlebih dahulu.")
        if st.button("Kembali ke Login"):
            try:
                st.switch_page("app.py")
            except Exception:
                st.rerun()
        st.stop()
    return user


def require_role(role: str):
    user = require_login()
    if user["role"] != role:
        st.error("Kamu tidak punya akses ke halaman ini.")
        st.stop()
    return user
