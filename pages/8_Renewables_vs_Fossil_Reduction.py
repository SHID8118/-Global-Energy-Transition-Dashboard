# pages/8_Renewables_vs_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Renewables vs Fossil Reduction", page_icon="🔗")

st.title("🔗 Renewables Share vs Fossil Fuel Consumption")
st.markdown("""
This dashboard analyzes how renewable energy adoption correlates with fossil fuel consumption across countries.
""")

@st.cache_data

def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")

    # Keep only the necessary columns
    cols_needed = [
        "country", "year",
        "coal_consumption", "oil_consumption", "gas_consumption",
        "renewables_share_energy"
    ]
    df = df[cols_needed]

    # Filter for latest year with most complete data
    latest_year = df["year"].max()
    df_latest = df[df["year"] == latest_year].copy()

    # Compute total fossil fuel consumption (TWh)
    df_latest["fossil_consumption_twh"] = df_latest[[
        "coal_consumption", "oil_consumption", "gas_consumption"
    ]].sum(axis=1, skipna=True)

    df_latest = df_latest.dropna(subset=["renewables_share_energy", "fossil_consumption_twh"])

    return df_latest, latest_year

# Load data
df, latest_year = load_data()

# Scatter plot
fig = px.scatter(
    df,
    x="renewables_share_energy",
    y="fossil_consumption_twh",
    hover_name="country",
    title=f"Renewable Energy Share vs Fossil Fuel Consumption ({latest_year})",
    labels={
        "renewables_share_energy": "Renewables Share in Final Energy (%)",
        "fossil_consumption_twh": "Total Fossil Fuel Consumption (TWh)"
    },
    template="plotly_white"
)
fig.update_traces(marker=dict(size=10, color="green", opacity=0.7))
fig.update_layout(hovermode="closest")

st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown(f"""
    - This plot shows the relationship between **renewable energy share** and **fossil fuel consumption** for {latest_year}.
    - Countries with a **higher share of renewables** often tend to have **lower absolute fossil fuel usage**, but not always.
    - Some high fossil-consuming countries are still making progress on increasing their renewables share.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **File:** `owid-energy-data.xlsx`
    - **Columns Used:** `coal_consumption`, `oil_consumption`, `gas_consumption`, `renewables_share_energy`, `country`, `year`
    - **Source:** Our World in Data (OWID)
    """)
