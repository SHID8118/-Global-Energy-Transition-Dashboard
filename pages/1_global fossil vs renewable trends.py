import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Global Petroleum Production Analysis")

def load_and_process_data():
    # Read Excel file with appropriate settings
    df = pd.read_excel("data.xlsx", header=None, engine='openpyxl')
    
    # Extract year headers from second row (index 1)
    years = df.iloc[1, 1:].tolist()
    years = [int(y) for y in years]
    
    processed_data = []
    current_country = None

    for i in range(len(df)):
        # Skip initial rows
        if i < 2:
            continue
            
        # Detect country headers (rows followed by "Production")
        if i < len(df)-1 and df.iloc[i+1, 0] == "Production":
            current_country = df.iloc[i, 0]
            # Skip next row ("Production")
            i += 1
            continue
            
        # Process metric rows if we're in a country section
        if current_country:
            # Check if this is a metric row (starts with INTL code)
            if str(df.iloc[i, 0]).startswith('INTL'):
                metric_name = df.iloc[i, 0]
                # Extract values for each year
                for year_idx, year in enumerate(years):
                    value = df.iloc[i, year_idx + 1]
                    try:
                        value = float(value)
                    except:
                        value = 0.0  # Handle non-numeric values
                        
                    processed_data.append({
                        'Country': current_country,
                        'Year': year,
                        'Metric': metric_name,
                        'Value': value
                    })
    
    # Create DataFrame from processed data
    return pd.DataFrame(processed_data)

# Load data with caching
@st.cache_data
def load_data():
    return load_and_process_data()

df = load_data()

# App title and download section
st.title("🌍 Global Petroleum Production Analysis (1973-2023)")
with st.expander("📄 Download Data"):
    st.download_button(
        "Download Processed Data",
        df.to_csv(index=False),
        "petroleum_production.csv",
        "text/csv"
    )

# Sidebar controls
with st.sidebar:
    st.header("📊 Filter Options")
    selected_metrics = st.multiselect(
        "Select Metrics",
        df['Metric'].unique(),
        default=["INTL.S3-1 Total petroleum and other liquids (Mb/d)"]
    )
    selected_countries = st.multiselect(
        "Select Countries",
        df['Country'].unique(),
        default=["World", "United States", "Russian Federation", "China"]
    )
    chart_type = st.radio("Chart Type", ["Line Chart", "Area Chart"])

# Data filtering
filtered_df = df[
    (df['Metric'].isin(selected_metrics)) & 
    (df['Country'].isin(selected_countries))
]

# Create visualization
if not filtered_df.empty:
    if chart_type == "Line Chart":
        fig = px.line(
            filtered_df,
            x='Year',
            y='Value',
            color='Country',
            facet_row='Metric',
            title=f"Petroleum Production Trends ({', '.join(selected_metrics)})",
            labels={'Value': 'Million Barrels per Day (Mb/d)'}
        )
    else:
        fig = px.area(
            filtered_df,
            x='Year',
            y='Value',
            color='Country',
            facet_row='Metric',
            title=f"Petroleum Production Trends ({', '.join(selected_metrics)})",
            labels={'Value': 'Million Barrels per Day (Mb/d)'}
        )
    
    st.plotly_chart(fig, use_container_width=True)

# Add insights section
with st.expander("📌 Key Insights"):
    st.markdown("""
    - **Global Peak**: Total petroleum production appears to have peaked around 2019-2020
    - **Regional Differences**: Middle Eastern countries show more stability compared to volatile Russian production
    - **Decline**: Many developed countries show declining production trends after 2010
    """)
    
# Show raw data section
with st.expander("🔍 Raw Data Table"):
    st.dataframe(df, use_container_width=True)
