import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        .stApp { background: #f7f5ff; color: #1f2937; }
        [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #ede9fe; }
        .nl-card {
            background: #ffffff; border: 1px solid #e9d5ff; border-radius: 8px;
            padding: 18px; margin: 10px 0; box-shadow: 0 4px 16px rgba(88, 28, 135, 0.06);
        }
        .nl-title { font-size: 1.2rem; font-weight: 700; color: #4c1d95; margin-bottom: 6px; }
        .nl-muted { color: #6b7280; font-size: 0.94rem; }
        .nl-badge {
            display: inline-block; padding: 4px 10px; border-radius: 999px;
            font-size: 0.78rem; font-weight: 700; margin: 2px 0;
        }
        .badge-done { background: #dcfce7; color: #166534; }
        .badge-active { background: #ede9fe; color: #5b21b6; }
        .badge-locked { background: #f3f4f6; color: #6b7280; }
        .metric-card {
            background: #ffffff; border-left: 5px solid #22c55e; border-radius: 8px;
            padding: 14px; margin: 8px 0; border-top: 1px solid #dcfce7;
            border-right: 1px solid #dcfce7; border-bottom: 1px solid #dcfce7;
        }
        .metric-card .value { font-size: 1.8rem; font-weight: 800; color: #4c1d95; }
        .metric-card .label { color: #6b7280; font-size: 0.9rem; }
        .feedback-ok { background: #dcfce7; border: 1px solid #86efac; color: #166534; padding: 12px; border-radius: 8px; }
        .feedback-bad { background: #fee2e2; border: 1px solid #fecaca; color: #991b1b; padding: 12px; border-radius: 8px; }
        div.stButton > button {
            border-radius: 8px; border: 1px solid #7c3aed; background: #7c3aed; color: white;
            font-weight: 700;
        }
        div.stButton > button:hover { border-color: #22c55e; background: #22c55e; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar_user():
    user = st.session_state.get("user")
    if not user:
        return
    st.sidebar.markdown(f"**{user['name']}**")
    st.sidebar.caption(f"Role: {user['role']}")


def badge(label: str, status: str):
    classes = {"Selesai": "badge-done", "Aktif": "badge-active", "Terkunci": "badge-locked"}
    klass = classes.get(label, status)
    return f"<span class='nl-badge {klass}'>{label}</span>"


def course_card(title, description, level, percent):
    st.markdown(
        f"""
        <div class="nl-card">
          <div class="nl-title">{title}</div>
          <div class="nl-muted">{description}</div>
          <p><b>Level:</b> {level}</p>
          <div class="nl-muted">Progress total: {percent}%</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def lesson_card(title, description, badge_html, done, total):
    percent = int((done / total) * 100) if total else 100
    st.markdown(
        f"""
        <div class="nl-card">
          <div class="nl-title">{title}</div>
          {badge_html}
          <div class="nl-muted">{description}</div>
          <p>{done}/{total} task selesai</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(percent)


def metric_card(label, value):
    st.markdown(
        f"<div class='metric-card'><div class='value'>{value}</div><div class='label'>{label}</div></div>",
        unsafe_allow_html=True,
    )
