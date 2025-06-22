import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(
    layout="wide",
    page_title="Global Oil Production Dashboard",
    page_icon="⛽"
)

@st.cache_data
def load_data():
    # Read the Excel file with proper handling
    df = pd.read_excel(
        "INT-Export-04-03-2025_21-40-52.xlsx",
        skiprows=1,        # Skip metadata row
        header=0,          # Use next row as header
        dtype=str
    )
    
    # Clean column names
    df.columns = [str(col).strip() for col in df.columns]
    
    # Rename first two columns
    df = df.rename(columns={df.columns[0]: "series_code", df.columns[1]: "series_name"})
    
    # Identify country rows (where series_code is NaN but series_name exists)
    country_mask = df['series_code'].isna() & df['series_name'].notna()
    df['country'] = df.loc[country_mask, 'series_name'].ffill()
    
    # Filter to only production data rows
    df = df[df['series_name'].str.contains('Production|Crude|Total|Refinery|NGPL|other liquids', na=False, case=False)]
    
    # Melt to long format
    year_cols = [col for col in df.columns if re.fullmatch(r"\d{4}", str(col))]
    df_long = df.melt(
        id_vars=["series_code", "series_name", "country"],
        value_vars=year_cols,
        var_name="year",
        value_name="value"
    )
    
    # Convert types
    df_long["year"] = df_long["year"].astype(int)
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
    
    return df_long.dropna(subset=["value"])

df = load_data()

# Sidebar controls
st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    options=df['country'].unique(),
    default=["World"]
)

selected_series = st.sidebar.multiselect(
    "Select Series",
    options=df['series_name'].unique(),
    default=[
        "Total petroleum and other liquids (Mb/d)",
        "Crude oil including lease condensate (Mb/d)"
    ]
)

# Filter data based on selections
filtered_df = df[
    (df['country'].isin(selected_countries)) & 
    (df['series_name'].isin(selected_series))
]

# Main dashboard
st.title("🌍 Global Petroleum Production Dashboard")
st.markdown("Analyze production trends across countries and metrics (1973-2023)")

# Plot trends
if not filtered_df.empty:
    fig = px.line(
        filtered_df,
        x="year",
        y="value",
        color="series_name",
        line_dash="country",
        title="Production Trends Over Time",
        labels={"value": "Production (Mb/d)", "year": "Year"},
        facet_col="country" if len(selected_countries) > 1 else None,
        facet_col_wrap=2
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected filters")

# Show raw data
with st.expander("📊 View Raw Data"):
    st.dataframe(filtered_df.sort_values(["country", "series_name", "year"]))

# Key metrics
with st.expander("🔑 Key Insights"):
    st.markdown("""
    - **Total petroleum and other liquids** includes all liquid fuels
    - **Crude oil including lease condensate** represents pure oil production
    - **NGPL** = Natural Gas Plant Liquids
    - Production drops visible in 2020 reflect COVID-19 impacts
    - World production has grown steadily despite periodic disruptions
    """)

# Add download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="oil_production_data.csv",
    mime="text/csv"
)
