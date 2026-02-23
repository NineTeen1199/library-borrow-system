import streamlit as st   

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="ระบบหอสมุด",
    page_icon="📚",
    layout="wide"
)
# =========================
# Hide Default Sidebar Menu
# =========================
st.markdown("""
<style>
section[data-testid="stSidebarNav"] {display: none;}
div[data-testid="stSidebarNav"] {display: none;}
nav[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)
# =========================
# Custom CSS (Modern Style)
# =========================
st.markdown("""
<style>

/* ===== Animated Background ===== */
.stApp {
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #0f2027, #203a43);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* ===== Glass Container ===== */
.block-container {
    background: rgba(255,255,255,0.05);
    padding: 2rem;
    border-radius: 20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* ===== Buttons ===== */
div.stButton > button {
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: bold;
    background: linear-gradient(45deg,#00c6ff,#0072ff);
    color: white;
    border: none;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #00c6ff;
}

/* ===== Divider ===== */
hr {
    border: 1px solid rgba(255,255,255,0.2);
}

</style>
""", unsafe_allow_html=True)

# =========================
# Import Pages
# =========================
from pages import book_page
from pages import member_page
from pages import borrow_page
from pages import admin_page
from pages import login_page
from pages import report_page


# =========================
# Session State
# =========================
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "books"


# =========================
# Login Gate
# =========================
if not st.session_state.is_logged_in:
    login_page.render_login()
    st.stop()


# =========================
# Header
# =========================
st.markdown("""
<div style="
    padding:25px;
    border-radius:20px;
    text-align:center;
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    box-shadow:0 8px 20px rgba(0,0,0,0.4);
    margin-bottom:30px;
">
    <h1>📚 ระบบหอสมุดอัจฉริยะ</h1>
    <p style='font-size:18px;'>Smart Library Borrow & Return System</p>
</div>
""", unsafe_allow_html=True)


# =========================
# Top Navigation Menu
# =========================
user = st.session_state.get("user") or {}
role = user.get("role", "staff")

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("📚 หนังสือ", use_container_width=True):
        st.session_state.page = "books"
        st.rerun()

with col2:
    if st.button("👤 สมาชิก", use_container_width=True):
        st.session_state.page = "members"
        st.rerun()

with col3:
    if st.button("🔄 ยืม-คืน", use_container_width=True):
        st.session_state.page = "borrows"
        st.rerun()

if role == "admin":
    with col4:
        if st.button("📊 รายงาน", use_container_width=True):
            st.session_state.page = "reports"
            st.rerun()

    with col5:
        if st.button("🛠️ จัดการผู้ใช้", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()

with col6:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.user = None
        st.session_state.page = "books"
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)


# =========================
# Routing
# =========================
if st.session_state.page == "books":
    book_page.render_book_page()

elif st.session_state.page == "members":
    member_page.render_member_page()

elif st.session_state.page == "borrows":
    borrow_page.render_borrow()

elif st.session_state.page == "reports":
    if role != "admin":
        st.warning("⚠️ Admin Only")
        st.session_state.page = "books"
        st.rerun()
    report_page.render_report()

elif st.session_state.page == "admin":
    if role != "admin":
        st.warning("⚠️ Admin Only")
        st.session_state.page = "books"
        st.rerun()
    admin_page.render_admin()

else:
    book_page.render_book_page()


# =========================
# Footer
# =========================
st.markdown("""
<hr>
<center>
<p style='font-size:14px; color:rgba(255,255,255,0.7);'>
👤 ผู้ใช้: {username} | 🔑 บทบาท: {role}
</p>
<p style='font-size:13px; color:rgba(255,255,255,0.5);'>
© 2026 Smart Library System
</p>
</center>
""".format(username=user.get("username","-"), role=role), unsafe_allow_html=True)