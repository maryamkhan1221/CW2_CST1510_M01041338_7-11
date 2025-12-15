import streamlit as st
from datetime import datetime

# LOGIN PROTECTION - MUST BE FIRST
# Block access to this page unless the user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

# Configure Streamlit page settings (title + wide layout)
st.set_page_config(page_title="Settings", layout="wide")

# Page heading + description
st.title("⚙️ Application Settings")
st.markdown("Manage your dashboard preferences and configurations")

# Sidebar divider
st.sidebar.markdown("---")

# Logout button (reset login state and rerun the app)
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# Main page divider line
st.markdown("---")

# Create tabs for organizing settings sections
tab1, tab2, tab3, tab4 = st.tabs(["Display", "Data", "Notifications", "User Profile"])

# TAB 1: DISPLAY SETTINGS
with tab1:
    st.subheader("Display Settings")
    
    # Two-column layout for display-related controls
    col1, col2 = st.columns(2)
    
    with col1:
        # Theme selection (light/dark/auto)
        theme = st.radio("Application Theme", options=["Light", "Dark", "Auto"], horizontal=False)

        # Page width preference
        page_width = st.select_slider("Page Width", options=["Narrow", "Normal", "Wide"], value="Normal")

        # Font size preference
        font_size = st.slider("Font Size", min_value=10, max_value=18, value=14, step=1)
    
    with col2:
        # Auto-refresh preference
        refresh_interval = st.selectbox(
            "Auto-refresh Interval",
            options=["Never", "30 seconds", "1 minute", "5 minutes", "15 minutes"],
            index=2
        )

        # Toggle animations on/off
        animations = st.checkbox("Enable Animations", value=True)

        # Toggle compact mode on/off
        compact_mode = st.checkbox("Compact Mode", value=False)
    
    # Save button for display settings (currently just shows success message)
    if st.button("💾 Save Display Settings", key="save_display"):
        st.success("✅ Display settings saved successfully!")

# Divider line between sections
st.markdown("---")

# TAB 2: DATA SETTINGS
with tab2:
    st.subheader("Data & Database Settings")
    
    # Two-column layout for data-related controls
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Data Source Configuration")

        # Directory path to locate datasets/files
        data_path = st.text_input("Data Directory Path", value="DATA/")

        # CSV parsing delimiter selection
        csv_delimiter = st.selectbox("CSV Delimiter", options=[",", ";", "\t", "|"])

        # File encoding selection
        encoding = st.selectbox("File Encoding", options=["utf-8", "utf-16", "latin-1", "ascii"])
    
    with col2:
        st.subheader("Data Processing")

        # Cache duration for data loading/processing
        cache_duration = st.slider("Cache Duration (minutes)", min_value=1, max_value=60, value=10, step=1)

        # Limit for how many rows are displayed in tables
        max_rows = st.number_input("Max Rows to Display", min_value=10, max_value=1000, value=100, step=10)

        # Toggle data validation on/off
        data_validation = st.checkbox("Enable Data Validation", value=True)
    
    # Save button for data settings (currently just shows success message)
    if st.button("💾 Save Data Settings", key="save_data"):
        st.success("✅ Data settings saved successfully!")

# Divider line between sections
st.markdown("---")

# TAB 3: NOTIFICATIONS
with tab3:
    st.subheader("Notification Settings")
    
    # Two-column layout for notification preferences + channels
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Alert Preferences")

        # Alert severity toggles
        critical_alerts = st.checkbox("🔴 Critical Alerts", value=True)
        high_alerts = st.checkbox("🟠 High Priority Alerts", value=True)
        medium_alerts = st.checkbox("🟡 Medium Priority Alerts", value=False)
        low_alerts = st.checkbox("🟢 Low Priority Alerts", value=False)
    
    with col2:
        st.subheader("Notification Channels")

        # Email notifications toggle + input field
        email_enabled = st.checkbox("📧 Email Notifications", value=True)
        if email_enabled:
            email_address = st.text_input("Email Address", placeholder="user@example.com")
        
        # Slack notifications toggle + webhook input field
        slack_enabled = st.checkbox("💬 Slack Notifications", value=False)
        if slack_enabled:
            slack_webhook = st.text_input("Slack Webhook URL", type="password", placeholder="https://hooks.slack.com/...")
        
        # Desktop notifications toggle
        desktop_enabled = st.checkbox("🖥️ Desktop Notifications", value=True)
    
    # Save button for notifications (currently just shows success message)
    if st.button("💾 Save Notification Settings", key="save_notifications"):
        st.success("✅ Notification settings saved successfully!")

# Divider line between sections
st.markdown("---")

# TAB 4: USER PROFILE
with tab4:
    st.subheader("User Profile Settings")
    
    # Two-column layout for profile and preferences
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Account Information")

        # Basic user profile fields
        full_name = st.text_input("Full Name", value="", placeholder="Enter your full name")
        user_email = st.text_input("Email Address", value="", placeholder="user@example.com")

        # Department selection
        department = st.selectbox(
            "Department",
            options=["IT Operations", "Cybersecurity", "Data Science", "Management", "Other"]
        )
    
    with col2:
        st.subheader("Preferences")

        # Role selection (UI only)
        role = st.selectbox("User Role", options=["Viewer", "Analyst", "Administrator"])

        # Language preference
        language = st.selectbox("Language", options=["English", "Spanish", "French", "German", "Arabic", "Chinese"])

        # Timezone selection (default index=5 => "GST")
        timezone = st.selectbox("Timezone", options=["UTC", "EST", "CST", "MST", "PST", "GST"], index=5)
    
    # Visual divider between profile settings and security settings
    st.divider()
    
    st.subheader("Security")

    # Password inputs (UI only; no actual password change logic here)
    col1, col2 = st.columns(2)
    
    with col1:
        current_password = st.text_input("Current Password", type="password")
    with col2:
        st.write("")  # spacer
    
    col1, col2 = st.columns(2)
    with col1:
        new_password = st.text_input("New Password", type="password")
    with col2:
        confirm_password = st.text_input("Confirm Password", type="password")
    
    # 2FA enable toggle (UI only)
    two_fa_enabled = st.checkbox("🔐 Enable Two-Factor Authentication", value=False)
    
    # Save button for profile settings (currently just shows success message)
    if st.button("💾 Save Profile Settings", key="save_profile"):
        st.success("✅ Profile settings saved successfully!")

# Final divider line
st.markdown("---")

# Footer text with version and last-updated timestamp
st.markdown(
    f"<p style='text-align: center; color: gray; font-size: 11px;'>"
    f"Week 10 Dashboard v1.0 | Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    f"</p>",
    unsafe_allow_html=True
)
