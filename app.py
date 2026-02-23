import streamlit as st

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
# Page Config
# =========================
st.set_page_config(
    page_title="ระบบยืม-คืนหนังสือ",
    page_icon="📚",
    layout="wide"
)

# =========================
# ซ่อนเมนู Multipage Streamlit
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
# Header
# =========================
st.title("📚 ระบบยืม-คืนหนังสือ")


# =========================
# Helper Menu Button
# =========================
def nav_button(label, key, icon=""):
    if st.sidebar.button(f"{icon} {label}", use_container_width=True):
        st.session_state.page = key
        st.rerun()


# =========================
# User Info
# =========================
user = st.session_state.get("user") or {}
role = user.get("role", "staff")

st.sidebar.markdown(f"👤 ผู้ใช้: **{user.get('username','-')}**")
st.sidebar.markdown(f"🔑 บทบาท: **{role}**")


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

# ⭐ Admin Only Menu
if role == "admin":
    nav_button("รายงาน", "reports", "📊")
    nav_button("จัดการผู้ใช้", "admin", "🛠️")


# =========================
# Routing + Guard
# =========================

# ---------- Books ----------
if st.session_state.page == "books":
    book_page.render_book_page()

# ---------- Members ----------
elif st.session_state.page == "members":
    member_page.render_member_page()

# ---------- Borrow ----------
elif st.session_state.page == "borrows":
    borrow_page.render_borrow()

# ---------- Reports (Admin Only) ----------
elif st.session_state.page == "reports":

    if role != "admin":
        st.warning("⚠️ หน้านี้สำหรับ Admin เท่านั้น")
        st.session_state.page = "books"
        st.rerun()

    report_page.render_report()

# ---------- Admin Page ----------
elif st.session_state.page == "admin":

    if role != "admin":
        st.warning("⚠️ หน้านี้สำหรับ Admin เท่านั้น")
        st.session_state.page = "books"
        st.rerun()

    admin_page.render_admin()

# ---------- Default ----------
else:
    book_page.render_book_page()
