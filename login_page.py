# pages/login_page.py
import streamlit as st
import controller

# =========================
# Custom Button CSS (Login)
# =========================
st.markdown("""
<style>

/* ปุ่ม Login */
div.stForm button {
    background-color: #00BFFF !important;  /* ฟ้า */
    color: white !important;
    font-weight: 800 !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 20px !important;
    transition: 0.3s ease !important;
}

/* Hover เป็นสีดำ */
div.stForm button:hover {
    background-color: black !important;
    color: white !important;
}

/* ตอนกด */
div.stForm button:active {
    background-color: #111 !important;
}

</style>
""", unsafe_allow_html=True)


def render_login():
    st.title("🔐 เข้าสู่ระบบ")

    # 👇 เพิ่มชื่อใต้หัวข้อ
    st.markdown(
        "<p style='font-size:16px; font-weight:bold;'>"
        "นาย อภิวัฒน์ พุ่มแดง  6740259122  ว.6706"
        "</p>",
        unsafe_allow_html=True
    )

    with st.form("login_form"):
        username = st.text_input(
            "ชื่อผู้ใช้",
            placeholder="เช่น admin"
        )
        password = st.text_input(
            "รหัสผ่าน",
            type="password",
            placeholder="เช่น 1234"
        )
        submitted = st.form_submit_button("Login")

    if submitted:
        ok, msgs, user_info = controller.login(username, password)

        if not ok:
            for m in msgs:
                st.error(m)
        else:
            for m in msgs:
                st.success(m)

            st.session_state["is_logged_in"] = True
            st.session_state["user"] = user_info
            st.session_state["page"] = "books"
            st.rerun()