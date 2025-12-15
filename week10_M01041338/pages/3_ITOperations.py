import streamlit as st
import pandas as pd
import plotly.express as px

# LOGIN PROTECTION - MUST BE FIRST
# Stop users from viewing this page unless logged_in is True in session state
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

# Configure Streamlit page settings (title + wide layout)
st.set_page_config(page_title="IT Operations", layout="wide")

# Page heading + short description
st.title("⚙️ IT Operations & Ticket Management")
st.markdown("Track and manage IT support tickets and operations metrics")

# Sample data (demo ticket dataset)
df_tickets = pd.DataFrame({
    'ticket_id': [f'TKT-{i:05d}' for i in range(1, 101)],  # ticket IDs
    'created_date': pd.date_range(start='2024-01-01', periods=100, freq='h'),  # hourly timestamps
    'priority': (['Critical', 'High', 'Medium', 'Low'] * 25)[:100],  # repeating priorities
    'category': (['Hardware', 'Software', 'Network', 'Account', 'Database'] * 20)[:100],  # repeating categories
    'status': (['Open', 'In Progress', 'Resolved', 'Closed'] * 25)[:100],  # repeating status values
    'assigned_to': (['Team A', 'Team B', 'Team C', 'Team D'] * 25)[:100],  # repeating team assignments
    'resolution_time_hours': list(range(1, 101))  # demo resolution times (1..100)
})

# Inform the user that this page uses sample/demo data
st.info("📊 Using sample data for demonstration")

# Sidebar separator
st.sidebar.markdown("---")

# Logout button (resets session flag + reruns app)
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# Sidebar filters section
st.sidebar.subheader("Filters")

# Filter: priorities to include
priority_filter = st.sidebar.multiselect(
    "Priority",
    options=df_tickets['priority'].unique(),
    default=df_tickets['priority'].unique()
)

# Filter: statuses to include
status_filter = st.sidebar.multiselect(
    "Status",
    options=df_tickets['status'].unique(),
    default=df_tickets['status'].unique()
)

# Apply filters to tickets dataframe
filtered_tickets = df_tickets[
    (df_tickets['priority'].isin(priority_filter)) &
    (df_tickets['status'].isin(status_filter))
]

# KPI Section (top summary metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Tickets", len(filtered_tickets))  # total after filtering
col2.metric("Open/In Progress", len(filtered_tickets[filtered_tickets['status'].isin(['Open', 'In Progress'])]))  # active tickets
col3.metric("Critical Tickets", len(filtered_tickets[filtered_tickets['priority'] == 'Critical']))  # critical priority
col4.metric(
    "Avg Resolution Time",
    f"{filtered_tickets['resolution_time_hours'].mean():.1f}h" if len(filtered_tickets) > 0 else "N/A"
)  # average resolution time (safe when empty)

# Divider before charts
st.markdown("---")

# Charts section (Plotly visualizations)
try:
    # Row 1: status pie + priority bar
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tickets by Status")

        # Count tickets per status
        status_data = filtered_tickets['status'].value_counts().reset_index()
        status_data.columns = ['status', 'count']

        # Pie chart showing status distribution
        fig1 = px.pie(
            status_data,
            values='count',
            names='status',
            color_discrete_sequence=['#ff6b6b', '#ffd93d', '#6bcf7f', '#4d96ff']
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Tickets by Priority")

        # Count tickets per priority
        priority_data = filtered_tickets['priority'].value_counts().reset_index()
        priority_data.columns = ['priority', 'count']

        # Bar chart showing priority counts
        fig2 = px.bar(priority_data, x='priority', y='count',
                     labels={'priority': 'Priority', 'count': 'Count'})
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: category bar + team bar
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tickets by Category")

        # Count tickets per category
        category_data = filtered_tickets['category'].value_counts().reset_index()
        category_data.columns = ['category', 'count']

        # Bar chart showing category counts
        fig3 = px.bar(category_data, x='category', y='count',
                     labels={'category': 'Category', 'count': 'Count'})
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("Tickets by Team")

        # Count tickets per assigned team
        team_data = filtered_tickets['assigned_to'].value_counts().reset_index()
        team_data.columns = ['team', 'count']

        # Bar chart showing tickets per team
        fig4 = px.bar(team_data, x='team', y='count',
                     labels={'team': 'Team', 'count': 'Count'})
        st.plotly_chart(fig4, use_container_width=True)
    
    # Row 3: timeline line + resolution time boxplot
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Tickets Over Time")

        # Group tickets by date and count them
        timeline_data = filtered_tickets.groupby(filtered_tickets['created_date'].dt.date).size().reset_index()
        timeline_data.columns = ['date', 'count']

        # Line chart showing ticket volume over time
        fig5 = px.line(
            timeline_data,
            x='date',
            y='count',
            markers=True,
            labels={'date': 'Date', 'count': 'Tickets'}
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        st.subheader("Resolution Time by Priority")

        # Box plot showing distribution of resolution times per priority
        fig6 = px.box(
            filtered_tickets,
            y='resolution_time_hours',
            x='priority',
            labels={'resolution_time_hours': 'Hours', 'priority': 'Priority'}
        )
        st.plotly_chart(fig6, use_container_width=True)

except Exception as e:
    # Catch chart errors so the page does not crash
    st.error(f"Chart error: {str(e)}")

# Divider before data table
st.markdown("---")

# Ticket details table
st.subheader("Ticket Details")
st.dataframe(filtered_tickets, use_container_width=True, hide_index=True)
