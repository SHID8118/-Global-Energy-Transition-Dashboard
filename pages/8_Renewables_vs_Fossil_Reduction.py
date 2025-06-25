# pages/8_Renewables_vs_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Renewables vs Fossil Reduction", page_icon="🔗")

st.title("🔗 Renewable Share vs Fossil Fuel Consumption")
st.markdown("""
This dashboard explores how **renewable energy growth** correlates with **fossil fuel consumption**.
Data is from the most recent year available.
""")

@st.cache_data

def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    df = df[df["year"] == df["year"].max()]  # filter for latest year

    df = df[[
        "country",
        "coal_consumption",
        "oil_consumption",
        "gas_consumption",
        "renewables_share_energy"
    ]]

    # Drop aggregates like 'World', 'Asia', etc.
    exclude = ["World", "Asia", "Africa", "Europe", "North America", "South America", "European Union"]
    df = df[~df["country"].isin(exclude)]

    # Drop rows with missing values
    df = df.dropna(subset=["renewables_share_energy"])

    # Calculate total fossil consumption
    df["fossil_total"] = df[["coal_consumption", "oil_consumption", "gas_consumption"]].sum(axis=1)

    return df

# Load
df = load_data()

# Scatter Plot
fig = px.scatter(
    df,
    x="renewables_share_energy",
    y="fossil_total",
    hover_name="country",
    labels={
        "renewables_share_energy": "Renewable Share (%)",
        "fossil_total": "Fossil Fuel Consumption (TWh)"
    },
    title="Renewable Share vs Fossil Fuel Consumption (Latest Year)",
    color="renewables_share_energy",
    size="fossil_total"
)
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown("""
    - Countries with **higher renewable shares** often show **lower total fossil fuel use**.
    - Outliers may suggest countries with both high renewables and high energy demand.
    - This correlation can help identify leaders and laggards in the energy transition.
    """)

# Data Source
with st.expander("📊 Data Sources"):
    st.markdown("""
    - `owid-energy-data.xlsx`
    - Variables used: `coal_consumption`, `oil_consumption`, `gas_consumption`, `renewables_share_energy`
    - Filtered for the most recent year available.
    """)
