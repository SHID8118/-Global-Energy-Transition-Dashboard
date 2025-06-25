# pages/7_Renewables_vs_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(layout="wide", page_title="Ren vs Fossil Correlation", page_icon="🔗")

st.title("🔗 Renewable Energy Growth vs Fossil Fuel Reduction")
st.markdown("""
This dashboard explores how the growth of **renewable energy share** correlates with the **total fossil fuel consumption** by country.
It gives an indication of whether increased renewable adoption is linked to decreased reliance on fossil fuels.
""")

@st.cache_data
def load_data():
    # Load fossil data
    fos = pd.read_excel("data/owid-energy-data.xlsx")
    fos_latest = fos[fos["year"] == fos["year"].max()][["country", "coal_consumption", "oil_consumption", "gas_consumption"]]
    fos_latest["fossil_total"] = fos_latest[["coal_consumption", "oil_consumption", "gas_consumption"]].sum(axis=1)

    # Load renewables share data
    ren = pd.read_excel("data/Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx", skiprows=3)
    ren.columns = ren.columns.str.strip()
    ren = ren.rename(columns={"Share of modern renewables": "renewables_share", "Year": "year", "Entity": "country"})
    ren_latest = ren[ren["year"] == ren["year"].max()][["country", "renewables_share"]]

    # Merge datasets
    df = fos_latest.merge(ren_latest, on="country", how="inner")
    df.dropna(subset=["renewables_share", "fossil_total"], inplace=True)
    return df

# Load and process
df = load_data()

# Data Preview
st.subheader("Data Preview")
st.dataframe(df.head())

# Scatter Plot
fig = px.scatter(
    df,
    x="renewables_share",
    y="fossil_total",
    hover_name="country",
    title="Renewable Share vs Fossil Consumption",
    labels={
        "renewables_share": "Renewable Share (%)",
        "fossil_total": "Total Fossil Fuel Consumption (TWh)"
    },
    size_max=60
)
fig.update_traces(marker=dict(color="green", size=10, opacity=0.7))
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

# Insights
with st.expander("📌 Key Insights"):
    st.markdown("""
    - Countries with **higher renewable shares** tend to show **lower fossil fuel consumption**, suggesting successful energy transition.
    - Some **outliers** may have high renewable shares but still large fossil consumption due to population or industrial demand.
    - The chart allows comparing **relative positioning** of countries in the clean energy transition.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **Fossil Fuel Data:** `owid-energy-data.xlsx` (Our World in Data)
    - **Renewable Share:** `Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx`
    - Year used: Most recent available for both datasets (e.g., 2022 or 2023)
    """)
