# Page: Global Energy Intensity vs GDP
# Version 1: For GDP (not PPP)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Energy Intensity vs GDP",
    layout="wide",
    page_icon="📉"
)

st.title("📉 Global Energy Intensity Over Time (GDP-based)")
st.markdown("""
This dashboard visualizes the change in global **energy intensity** over time,
based on **GDP** (not adjusted for purchasing power parity).
Energy intensity is expressed in **MJ per thousand 2015 USD**.
""")

@st.cache_data
def load_data():
    df = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-World.xlsx", skiprows=3)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

if "Year" not in df.columns or "TES/GDP" not in df.columns:
    st.error("Expected columns 'Year' and 'TES/GDP' not found in the Excel file.")
    st.stop()

# Filter and convert
plot_df = df[["Year", "TES/GDP"]].dropna()
plot_df["Year"] = pd.to_numeric(plot_df["Year"], errors="coerce").astype("Int64")
plot_df["TES/GDP"] = pd.to_numeric(plot_df["TES/GDP"], errors="coerce")
plot_df = plot_df.dropna()

# Chart
fig = px.line(
    plot_df,
    x="Year",
    y="TES/GDP",
    title="Global Energy Intensity (MJ per 1,000 USD GDP)",
    labels={"Year": "Year", "TES/GDP": "MJ per 1,000 USD"},
    markers=True
)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown("""
    - Shows how efficiently the world uses energy relative to **GDP (not PPP)**.
    - A **downward trend** indicates improved energy efficiency.
    - Useful for tracking **sustainability progress** relative to economic activity.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **File:** `Total-energy-supply-_TES_-by-GDP-World.xlsx`
    - **Columns:** `Year`, `TES/GDP`
    - Data reflects energy use per GDP, **not adjusted for PPP**.
    """)
