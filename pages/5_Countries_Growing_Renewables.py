# pages/5_Global_Energy_Intensity_vs_GDP.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Global Energy Intensity vs GDP",
    layout="wide",
    page_icon="📉"
)

st.title("📉 Global Energy Intensity Over Time")
st.markdown("""
This dashboard visualizes the change in global **energy intensity** — the amount of energy used per unit of economic output —
over time. Energy intensity here is expressed in **MJ per thousand 2015 USD (PPP)**.
""")

@st.cache_data
def load_data():
    # Skip the first 3 metadata rows; real data starts from row 4
    df = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-World.xlsx", skiprows=3)
    # Clean column names
    df.columns = df.columns.str.strip()
    return df

# Load
df = load_data()

# Ensure the expected columns are present
if "Year" not in df.columns or "TES/GDP" not in df.columns:
    st.error("Expected columns 'Year' and 'TES/GDP' not found in the Excel file.")
    st.stop()

# Prepare DataFrame for plotting
df = df[["Year", "TES/GDP"]].dropna()
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
df["TES/GDP"] = pd.to_numeric(df["TES/GDP"], errors="coerce")
df = df.dropna(subset=["Year", "TES/GDP"])

# Preview
st.subheader("Data Preview")
st.dataframe(df.head())

if df.empty:
    st.warning("No valid data available to display. Please check the Excel file format.")
    st.stop()

# Plot
fig = px.line(
    df,
    x="Year",
    y="TES/GDP",
    title="Global Energy Intensity (MJ per thousand 2015 USD PPP)",
    labels={
        "Year": "Year",
        "TES/GDP": "Energy Intensity (MJ per 1 000 USD PPP)"
    },
    markers=True
)
fig.update_traces(line_color="blue")
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown("""
    - **Energy intensity** measures how much energy is required to produce one unit of economic output.
    - A **declining trend** means the global economy is becoming more energy-efficient or shifting to less energy-intensive activities.
    - Tracking energy intensity helps assess progress toward decoupling energy use from economic growth.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **File:** `data/Total-energy-supply-_TES_-by-GDP-World.xlsx`  
    - **Columns used:** `Year`, `TES/GDP` (in MJ per thousand 2015 USD PPP)  
    - Data sourced from the International Energy Agency (IEA) or Our World in Data.
    """)
