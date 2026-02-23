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
# Custom CSS Theme
# =========================
st.markdown("""
<style>

/* ===== Background ===== */
.stApp {
    background: linear-gradient(to right, #f4f6f9, #e8f0ff);
}

/* ===== Header ===== */
h1 {
    color: #1f4e79;
    font-weight: 700;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #1f4e79;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== Sidebar Buttons ===== */
div.stButton > button {
    border-radius: 10px;
    border: none;
    padding: 10px;
    font-weight: 600;
    transition: 0.3s;
}

div.stButton > button:hover {
    background-color: #4a90e2;
    color: white;
    transform: scale(1.03);
}

/* ===== Card Effect ===== */
.block-container {
    padding-top: 2rem;
}

hr {
    border: 1px solid #ddd;
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
# Hide Default Multipage Menu
# =========================
st.markdown("""
<style>
section[data-testid="stSidebarNav"] {display: none;}
div[data-testid="stSidebarNav"] {display: none;}
nav[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)


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
# Header Card
# =========================
st.markdown("""
<div style="
    background-color:#1f4e79;
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
    box-shadow:0px 4px 15px rgba(0,0,0,0.2);
">
    <h1>📚 ระบบหอสมุดโรงเรียน</h1>
    <p>Library Borrow & Return Management System</p>
</div>
""", unsafe_allow_html=True)


# =========================
# Helper Navigation Button
# =========================
def nav_button(label, key, icon=""):
    if st.sidebar.button(f"{icon} {label}", use_container_width=True):
        st.session_state.page = key
        st.rerun()


# =========================
# User Info Card
# =========================
user = st.session_state.get("user") or {}
role = user.get("role", "staff")

st.sidebar.markdown("""
<div style="
    background-color:#163d5c;
    padding:15px;
    border-radius:10px;
    text-align:center;
">
""", unsafe_allow_html=True)

st.sidebar.markdown(f"👤 **{user.get('username','-')}**")
st.sidebar.markdown(f"🔑 บทบาท: **{role}**")

st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.sidebar.divider()


# =========================
# Logout
# =========================
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.is_logged_in = False
    st.session_state.user = None
    st.session_state.page = "books"
    st.rerun()


# =========================
# Sidebar Menu
# =========================
st.sidebar.divider()

nav_button("หนังสือ", "books", "📚")
nav_button("สมาชิก", "members", "👤")
nav_button("ยืม-คืน", "borrows", "🔄")

# Admin Menu
if role == "admin":
    nav_button("รายงาน", "reports", "📊")
    nav_button("จัดการผู้ใช้", "admin", "🛠️")


# =========================
# Routing + Guard
# =========================

if st.session_state.page == "books":
    book_page.render_book_page()

elif st.session_state.page == "members":
    member_page.render_member_page()

elif st.session_state.page == "borrows":
    borrow_page.render_borrow()

elif st.session_state.page == "reports":

    if role != "admin":
        st.warning("⚠️ หน้านี้สำหรับ Admin เท่านั้น")
        st.session_state.page = "books"
        st.rerun()

    report_page.render_report()

elif st.session_state.page == "admin":

    if role != "admin":
        st.warning("⚠️ หน้านี้สำหรับ Admin เท่านั้น")
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
<p style='color:gray; font-size:14px;'>
© 2026 ระบบหอสมุด | พัฒนาโดย ทีม IT
</p>
</center>
""", unsafe_allow_html=True)