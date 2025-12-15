import streamlit as st
from app.services.user_service import login_user, register_user

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(
    page_title="Week 10 Dashboard - Login",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- LOGIN / REGISTER ----------------
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>📊 Week 10 Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Integrated Analytics Platform</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

        # -------- LOGIN (READ) --------
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login", use_container_width=True)

            if submit_button:
                success, result = login_user(username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = result
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error(result)

        # -------- REGISTER (CREATE) --------
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("New Username")
                new_password = st.text_input("New Password", type="password")
                register_button = st.form_submit_button("Register", use_container_width=True)

            if register_button:
                success, message = register_user(new_username, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)

# ---------------- DASHBOARD ----------------
else:
    st.set_page_config(page_title="Dashboard Home", layout="wide")

    st.sidebar.title("📊 Dashboard Navigation")
    st.sidebar.markdown(f"**Welcome, {st.session_state.username}!** 👋")
    st.sidebar.markdown("---")

    st.sidebar.page_link("pages/1_Cybersecurity.py", label="🛡️ Cybersecurity")
    st.sidebar.page_link("pages/2_DataScience.py", label="📊 Data Science")
    st.sidebar.page_link("pages/3_ITOperations.py", label="⚙️ IT Operations")
    st.sidebar.page_link("pages/4_Settings.py", label="⚙️ Settings")

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    st.title("📈 Week 10 Dashboard Home")
    st.markdown("Welcome to your integrated analytics platform.")

    st.markdown("---")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Incidents", "50")
    col2.metric("Critical Issues", "12")
    col3.metric("Open Tickets", "34")
    col4.metric("Avg Resolution", "2.5h")
    col5.metric("System Health", "95%")

    st.markdown("---")
    st.success(f"✅ Logged in as: **{st.session_state.username}**")
