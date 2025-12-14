import streamlit as st
import pandas as pd
import plotly.express as px

# LOGIN PROTECTION - MUST BE FIRST
# Prevent access unless the session indicates the user is logged in
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("❌ Please login first!")
    st.stop()

# Configure Streamlit page (title + wide layout)
st.set_page_config(page_title="Data Science Insights", layout="wide")

# Page heading and description
st.title("📊 Data Science Analytics")
st.markdown("Explore datasets and their metadata analysis")

# Sample data (metadata about multiple datasets)
df_metadata = pd.DataFrame({
    'dataset_name': ['Customer Sales', 'User Behavior', 'Product Inventory', 'Revenue Trends', 'Market Analysis'],
    'records': [10000, 50000, 5000, 8000, 15000],  # number of rows/records in each dataset
    'features': [25, 45, 30, 20, 35],  # number of columns/features in each dataset
    'missing_percentage': [2.5, 5.0, 1.2, 3.8, 4.5],  # missing values percentage estimate
    'last_updated': ['2024-01-31', '2024-02-29', '2024-03-31', '2024-04-30', '2024-05-31'],  # update timestamps
    'quality_score': [95, 87, 98, 91, 85]  # overall data quality score
})

# Notify the user that the page is using sample/demo data
st.info("📊 Using sample data for demonstration")

# Sidebar section divider
st.sidebar.markdown("---")

# Logout button (turn off logged_in and rerun)
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# Sidebar filters section
st.sidebar.subheader("Dataset Filters")

# Multiselect widget to choose which datasets to include
selected_datasets = st.sidebar.multiselect(
    "Select Datasets",
    options=df_metadata['dataset_name'].unique(),
    default=df_metadata['dataset_name'].unique()
)

# Filter the dataframe to only include selected datasets
filtered_metadata = df_metadata[df_metadata['dataset_name'].isin(selected_datasets)]

# KPI Section (top-level summary numbers)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Datasets", len(filtered_metadata))  # how many datasets are currently selected
col2.metric("Total Records", f"{filtered_metadata['records'].sum():,}")  # total records across selected datasets
col3.metric("Avg Quality Score", f"{filtered_metadata['quality_score'].mean():.1f}%")  # average quality score
col4.metric("Total Features", filtered_metadata['features'].sum())  # total features across selected datasets

# Divider before charts
st.markdown("---")

# Charts section (Plotly visualizations)
try:
    # First row: two charts side-by-side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Dataset Size Comparison")

        # Bar chart: dataset name vs record count (colored by quality score)
        fig1 = px.bar(
            filtered_metadata,
            x='dataset_name',
            y='records',
            color='quality_score',
            color_continuous_scale='Viridis',
            labels={'dataset_name': 'Dataset', 'records': 'Records'}
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Data Quality Scores")

        # Scatter plot: features vs quality score (bubble size based on records)
        fig2 = px.scatter(
            filtered_metadata,
            x='features',
            y='quality_score',
            size='records',
            labels={'features': 'Features', 'quality_score': 'Quality Score'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Second row: two charts side-by-side
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Missing Data Analysis")

        # Bar chart: dataset name vs missing percentage (colored by missing percentage)
        fig3 = px.bar(
            filtered_metadata,
            x='dataset_name',
            y='missing_percentage',
            color='missing_percentage',
            color_continuous_scale='Reds',
            labels={'dataset_name': 'Dataset', 'missing_percentage': 'Missing %'}
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        st.subheader("Features per Dataset")

        # Pie chart showing how features are distributed across datasets
        fig4 = px.pie(filtered_metadata, values='features', names='dataset_name')
        st.plotly_chart(fig4, use_container_width=True)

except Exception as e:
    # Handle unexpected errors during chart creation/rendering
    st.error(f"Chart error: {str(e)}")

# Divider before metadata table
st.markdown("---")

# Show filtered metadata table
st.subheader("Dataset Metadata")
st.dataframe(filtered_metadata, use_container_width=True, hide_index=True)

# Summary Statistics section (small table of derived totals/averages)
st.subheader("Summary Statistics")

# Build a small dataframe with key summary numbers
summary_stats = pd.DataFrame({
    'Metric': ['Total Records', 'Total Features', 'Avg Quality Score', 'Avg Missing %'],
    'Value': [
        f"{filtered_metadata['records'].sum():,}",
        f"{filtered_metadata['features'].sum()}",
        f"{filtered_metadata['quality_score'].mean():.2f}%",
        f"{filtered_metadata['missing_percentage'].mean():.2f}%"
    ]
})

# Display summary stats table
st.dataframe(summary_stats, use_container_width=True, hide_index=True)
