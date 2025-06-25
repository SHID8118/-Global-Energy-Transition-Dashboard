# pages/8_Renewables_vs_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Renewables vs Fossils", page_icon="♻️")

st.title("♻️ Renewable Share vs Fossil Fuel Consumption")
st.markdown("""
This dashboard explores the correlation between countries' share of **renewable energy** and their **fossil fuel consumption**.
We compare recent values of each and visualize their relationship.
""")

@st.cache_data
def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    df.columns = df.columns.str.lower()  # normalize columns

    # Use latest available year
    latest_year = df["year"].max()
    df = df[df["year"] == latest_year]

    # Select required columns
    cols_needed = [
        "country", "renewables_share_energy", "fossil_fuel_consumption"
    ]
    df = df[cols_needed]
    df = df.dropna()

    df = df.sort_values("renewables_share_energy", ascending=False)
    return df, latest_year

# Load and prepare data
df, latest_year = load_data()

# Plot
fig = px.scatter(
    df,
    x="renewables_share_energy",
    y="fossil_fuel_consumption",
    hover_name="country",
    labels={
        "renewables_share_energy": "Renewable Share (%)",
        "fossil_fuel_consumption": "Fossil Fuel Consumption (TWh)"
    },
    title=f"Renewable Share vs Fossil Consumption in {latest_year}"
)
fig.update_traces(marker=dict(size=10, color="green", opacity=0.7))
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

with st.expander("📌 Narrative"):
    st.markdown(f"""
    In **{latest_year}**, countries with higher **renewable shares** often show lower **fossil fuel consumption**, 
    although some high-consumption economies still rely heavily on fossil fuels despite adopting renewables.
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - **Source:** Our World in Data
    - **File:** `owid-energy-data.xlsx`
    - **Columns used:** `renewables_share_energy`, `fossil_fuel_consumption`, `country`, `year`
    """)
