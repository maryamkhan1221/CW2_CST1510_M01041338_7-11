import streamlit as st
import pandas as pd
import plotly.express as px
from app.data.incidents import (
    insert_incident,
    get_all_incidents,
    update_incident_status,
    delete_incident
)

# ---------------- LOGIN PROTECTION ----------------
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

st.set_page_config(page_title="Cybersecurity Analytics", layout="wide")

st.title("🛡️ Cybersecurity Incidents Dashboard")
st.markdown("Monitor and analyze cybersecurity incidents across your organization")

# ---------------- READ (DATABASE) ----------------
df_incidents = get_all_incidents()

if df_incidents.empty:
    st.warning("No incidents found in the database.")

st.sidebar.markdown("---")

# ---------------- LOGOUT ----------------
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# ---------------- CREATE ----------------
st.subheader("➕ Report New Incident")

with st.form("create_incident_form"):
    col1, col2, col3 = st.columns(3)

    with col1:
        date = st.date_input("Date")
        incident_type = st.selectbox("Type", ["Malware", "Phishing", "DDoS", "Data Breach"])

    with col2:
        severity = st.selectbox("Severity", ["Critical", "High", "Medium", "Low"])
        status = st.selectbox("Status", ["Investigating", "Contained", "Resolved"])

    with col3:
        reported_by = st.text_input("Reported By")

    description = st.text_area("Description")
    submit_incident = st.form_submit_button("Create Incident")

if submit_incident:
    insert_incident(date, incident_type, severity, status, description, reported_by)
    st.success("✅ Incident created successfully")
    st.rerun()

st.markdown("---")

# ---------------- FILTERS ----------------
st.sidebar.subheader("Filters")

severity_filter = st.sidebar.multiselect(
    "Severity Level",
    options=df_incidents["severity"].unique(),
    default=df_incidents["severity"].unique(),
)

filtered_df = (
    df_incidents[df_incidents["severity"].isin(severity_filter)]
    if severity_filter else df_incidents
)

# ---------------- METRICS ----------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Incidents", len(filtered_df))
col2.metric("Critical Issues", len(filtered_df[filtered_df["severity"] == "Critical"]))
col3.metric(
    "Resolved",
    f"{len(filtered_df[filtered_df['status'] == 'Resolved'])}/{len(filtered_df)}"
)
col4.metric("Avg Resolution", f"{filtered_df.index.size:.1f}")

st.markdown("---")

# ---------------- CHARTS (UNCHANGED LOGIC) ----------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Incidents by Severity")
    fig1 = px.pie(
        filtered_df,
        names="severity"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Incidents Over Time")
    timeline = filtered_df.groupby("date").size().reset_index(name="count")
    fig2 = px.line(timeline, x="date", y="count", markers=True)
    st.plotly_chart(fig2, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Incident Types")
    fig3 = px.bar(
        filtered_df["incident_type"].value_counts().reset_index(),
        x="incident_type",
        y="count"
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Status Distribution")
    fig4 = px.bar(
        filtered_df["status"].value_counts().reset_index(),
        x="status",
        y="count"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ---------------- UPDATE + DELETE ----------------
st.subheader("✏️ Manage Incidents")

selected_id = st.selectbox(
    "Select Incident ID",
    options=filtered_df["id"].tolist()
)

new_status = st.selectbox(
    "Update Status",
    ["Investigating", "Contained", "Resolved"]
)

col1, col2 = st.columns(2)

with col1:
    if st.button("Update Status"):
        update_incident_status(selected_id, new_status)
        st.success("✅ Incident status updated")
        st.rerun()

with col2:
    if st.button("Delete Incident"):
        delete_incident(selected_id)
        st.warning("🗑️ Incident deleted")
        st.rerun()

st.markdown("---")

# ---------------- TABLE ----------------
st.subheader("Incident Details")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# ---------------- ASSISTANT ----------------
from app.components.assistant_bot import render_assistant
render_assistant(filtered_df, "Cybersecurity")
