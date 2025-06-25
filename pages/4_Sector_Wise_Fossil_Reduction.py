# pages/4_Sector_Wise_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Sector Fossil Reduction",
    layout="wide",
    page_icon="🏭"
)

st.title("🏭 What Sectors Are Driving Fossil Fuel Reduction?")
st.markdown("""
This page explores which economic sectors—such as transport, industry, and power generation—have contributed most to the decline in fossil fuel consumption over time.
""")

@st.cache_data
def load_data():
    # Load the sector-specific dataset
    df = pd.read_excel("data/INT-Export-04-03-2025_21-40-52.xlsx")
    # Normalize column names
    df.columns = (
        df.columns
          .str.strip()
          .str.lower()
          .str.replace(r"\s+", "_", regex=True)
    )
    # Detect the year column
    year_col = next((c for c in df.columns if "year" in c), None)
    # Define possible sector columns
    possible_sectors = ["transport", "industry", "power", "electricity"]
    # Find which of these actually exist
    sectors = [c for c in possible_sectors if c in df.columns]
    # If no sectors found, return empty
    if year_col is None or not sectors:
        return pd.DataFrame(), year_col, sectors
    # Keep only year + sector columns
    df = df[[year_col] + sectors].dropna(subset=[year_col])
    df = df.rename(columns={year_col: "year"})
    # Convert year to int
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype(int)
    return df, "year", sectors

df, year_col, sectors = load_data()

if df.empty or not sectors:
    st.error("No sector columns found in the dataset. Please ensure the file has columns named ‘transport’, ‘industry’, or ‘power’/‘electricity’.")
    st.stop()

# Area chart of sector consumption
fig = px.area(
    df,
    x="year",
    y=sectors,
    title="Fossil Fuel Consumption by Sector Over Time",
    labels={"year": "Year", **{s: f"{s.capitalize()} Consumption" for s in sectors}}
)
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Narrative"):
    st.markdown(f"""
    - Among the sectors displayed, **{', '.join([s.capitalize() for s in sectors])}** are tracked.
    - The **area chart** above shows how each sector's fossil fuel consumption has evolved.
    - Steeper declines indicate sectors that are decarbonizing faster—typically the **power sector** (power/electricity) and **industry**.
    - **Transport** often lags due to slower fleet turnover and infrastructure changes.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **File:** `data/INT-Export-04-03-2025_21-40-52.xlsx`  
    - **Columns used:**  
      - `year` (detected automatically)  
      - Sector columns detected: **{transport, industry, power/electricity}**  
    - Ensure the file contains rows of annual fossil consumption by sector.
    """)
