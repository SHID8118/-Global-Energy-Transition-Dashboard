import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    layout="wide",
    page_title="Global Energy Intensity vs GDP",
    page_icon="📉"
)

st.title("📉 Global Energy Intensity vs GDP")

st.markdown("""
This dashboard visualizes the change in global **energy intensity** — 
defined as the amount of energy used per unit of economic output — over time.
""")

@st.cache_data
def load_data():
    df = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-World.xlsx")

    # Clean up column names
    df.columns = df.columns.str.strip()

    # Look for the correct columns
    intensity_col = [col for col in df.columns if "TES" in col and "GDP" in col]
    if not intensity_col or "Year" not in df.columns:
        st.error(f"Expected columns like 'Year' and 'TES (GJ per USD GDP PPP)' not found.")
        return pd.DataFrame()

    df = df[["Year", intensity_col[0]]].dropna()
    df = df.rename(columns={intensity_col[0]: "Energy Intensity (GJ/USD PPP)"})
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df["Energy Intensity (GJ/USD PPP)"] = pd.to_numeric(df["Energy Intensity (GJ/USD PPP)"], errors="coerce")
    df = df.dropna()
    
    return df

# Load data
df = load_data()

if df.empty:
    st.warning("No valid data available to display. Please check the Excel file format.")
    st.stop()

# Line chart
fig = px.line(
    df,
    x="Year",
    y="Energy Intensity (GJ/USD PPP)",
    title="Global Energy Intensity (GJ per USD PPP GDP) Over Time",
    labels={"Energy Intensity (GJ/USD PPP)": "GJ per USD (PPP)", "Year": "Year"},
    markers=True
)
fig.update_traces(line_color="green")
fig.update_layout(hovermode="x unified")

st.plotly_chart(fig, use_container_width=True)

# Key Takeaways
with st.expander("📌 What is Energy Intensity?"):
    st.markdown("""
    - **Energy intensity** measures how efficiently the economy uses energy.
    - It is calculated as **Total Energy Supply / GDP** (Purchasing Power Parity).
    - A **declining trend** indicates better energy efficiency or economic shifts to less energy-intensive sectors.
    - Tracking this helps evaluate global progress toward decoupling energy use from economic growth.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - File: `Total-energy-supply-_TES_-by-GDP-World.xlsx`
    - Data likely sourced from IEA or Our World in Data.
    """)
