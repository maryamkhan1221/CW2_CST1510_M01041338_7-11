import streamlit as st

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

st.set_page_config(
    page_title="Week 10 Dashboard - Login",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# If NOT logged in - show login page
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center;'>📊 Week 10 Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Integrated Analytics Platform</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit_button = st.form_submit_button("Login", use_container_width=True)
        
        if submit_button:
            if (username == "admin" and password == "admin123") or (username == "user" and password == "user123"):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
        
        st.markdown("---")
        st.info("**Demo Credentials:**\n\n- Username: `admin` | Password: `admin123`\n- Username: `user` | Password: `user123`")

# If logged in - show protected dashboard
else:
    st.set_page_config(page_title="Dashboard Home", layout="wide")
    
    st.sidebar.title("📊 Dashboard Navigation")
    st.sidebar.markdown(f"**Welcome, {st.session_state.username}!** 👋")
    st.sidebar.markdown("---")
    
    st.sidebar.page_link("pages/1_Cybersecurity.py", label="🛡️ Cybersecurity", icon="🛡️")
    st.sidebar.page_link("pages/2_DataScience.py", label="📊 Data Science", icon="📊")
    st.sidebar.page_link("pages/3_ITOperations.py", label="⚙️ IT Operations", icon="⚙️")
    st.sidebar.page_link("pages/4_Settings.py", label="⚙️ Settings", icon="⚙️")
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()
    
    st.title("📈 Week 10 Dashboard Home")
    st.markdown("Welcome to your integrated analytics platform. Monitor cybersecurity, data science, and IT operations in one place.")
    
    st.markdown("---")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Incidents", "50", delta="+3 today")
    col2.metric("Critical Issues", "12", delta="-2 from yesterday")
    col3.metric("Open Tickets", "34", delta="+5 new")
    col4.metric("Avg Resolution", "2.5h", delta="-0.5h")
    col5.metric("System Health", "95%", delta="+2%")
    
    st.markdown("---")
    st.success(f"✅ Logged in as: **{st.session_state.username}**")