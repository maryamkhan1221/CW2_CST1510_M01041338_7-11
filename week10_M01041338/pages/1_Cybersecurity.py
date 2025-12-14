import streamlit as st
import pandas as pd
import plotly.express as px

# LOGIN PROTECTION - MUST BE FIRST
# Stop users from accessing this page unless they are logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

# Configure the Streamlit page settings (title + wide layout)
st.set_page_config(page_title="Cybersecurity Analytics", layout="wide")

# Page header/title + short description text
st.title("🛡️ Cybersecurity Incidents Dashboard")
st.markdown("Monitor and analyze cybersecurity incidents across your organization")

# Create a sample dataset of cybersecurity incidents for demo purposes
df_incidents = pd.DataFrame({
    "incident_id": [f"INC-{i:04d}" for i in range(1, 51)],  # INC-0001 ... INC-0050
    "date": pd.date_range(start="2024-01-01", periods=50, freq="D"),  # 50 daily dates
    "severity": (["Critical", "High", "Medium", "Low"] * 13)[:50],  # repeating categories
    "type": (["Malware", "Phishing", "DDoS", "Data Breach"] * 13)[:50],  # repeating types
    "status": (["Resolved", "Investigating", "Contained"] * 17)[:50],  # repeating statuses
    "response_time_hours": ([2, 4, 6, 8, 12, 1, 3, 5, 7, 24] * 5)[:50],  # sample response times
})

# Inform the user that this page currently uses sample (not database) data
st.info("📊 Using sample data for demonstration")

# Sidebar separator line
st.sidebar.markdown("---")

# Logout button (resets the login flag and reloads the app)
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# Sidebar filter controls section
st.sidebar.subheader("Filters")

# Multi-select filter for incident severity levels
severity_filter = st.sidebar.multiselect(
    "Severity Level",
    options=df_incidents["severity"].unique(),
    default=df_incidents["severity"].unique(),
)

# Apply the severity filter if user selected any values; otherwise keep full dataset
filtered_df = df_incidents[df_incidents["severity"].isin(severity_filter)] if severity_filter else df_incidents

# KPI/metrics row (top summary tiles)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", len(filtered_df))  # total rows after filtering
col2.metric("Critical Issues", len(filtered_df[filtered_df["severity"] == "Critical"]))  # count critical only
col3.metric("Resolved", f"{len(filtered_df[filtered_df['status'] == 'Resolved'])}/{len(filtered_df)}")  # resolved count / total
col4.metric("Avg Response Time", f"{filtered_df['response_time_hours'].mean():.1f}h")  # average response time

# Divider line between metrics and charts
st.markdown("---")

try:
    # First row of charts (2 columns)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incidents by Severity")

        # Count incidents per severity
        severity_data = filtered_df["severity"].value_counts().reset_index()
        severity_data.columns = ["severity", "count"]

        # Pie chart showing severity distribution
        fig1 = px.pie(
            severity_data,
            values="count",
            names="severity",
            color_discrete_sequence=["#ff4444", "#ff8800", "#ffcc00", "#00cc44"],
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Incidents Over Time")

        # Group incidents by date and count them
        timeline_data = filtered_df.groupby(filtered_df["date"].dt.date).size().reset_index()
        timeline_data.columns = ["date", "count"]

        # Line chart showing incident counts by day
        fig2 = px.line(
            timeline_data,
            x="date",
            y="count",
            markers=True,
            labels={"date": "Date", "count": "Count"},
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Second row of charts (2 columns)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Incident Types")

        # Count incidents per type
        type_data = filtered_df["type"].value_counts().reset_index()
        type_data.columns = ["type", "count"]

        # Bar chart showing incident types
        fig3 = px.bar(type_data, x="type", y="count", labels={"type": "Type", "count": "Count"})
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.subheader("Status Distribution")

        # Count incidents per status
        status_data = filtered_df["status"].value_counts().reset_index()
        status_data.columns = ["status", "count"]

        # Bar chart showing status breakdown
        fig4 = px.bar(status_data, x="status", y="count", labels={"status": "Status", "count": "Count"})
        st.plotly_chart(fig4, use_container_width=True)

except Exception as e:
    # Catch any plotting/data errors and show them in the UI
    st.error(f"Chart error: {e}")

# Divider line before the data table
st.markdown("---")

# Show the filtered dataset in a table
st.subheader("Incident Details")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# Import and render the assistant chat component for this page
from app.components.assistant_bot import render_assistant
render_assistant(filtered_df, "Cybersecurity")
