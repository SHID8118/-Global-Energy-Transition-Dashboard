# pages/8_Renewables_vs_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Ren vs Fossil Correlation", page_icon="🔗")

@st.cache_data

def load_data():
    # Load both datasets
    fos = pd.read_excel("data/owid-energy-data.xlsx", sheet_name=0)
    ren = pd.read_excel("data/Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx", skiprows=3)

    # Clean column names
    fos.columns = fos.columns.str.strip().str.lower()
    ren.columns = ren.columns.str.strip().str.lower()

    # Filter latest year from OWID fossil data (keep relevant columns)
    latest_year = fos['year'].max()
    fos_latest = fos[fos['year'] == latest_year][[
        "country",
        "coal_consumption",
        "oil_consumption",
        "gas_consumption"
    ]].copy()

    # Create total fossil column
    fos_latest["fossil_total"] = fos_latest[["coal_consumption", "oil_consumption", "gas_consumption"]].sum(axis=1)

    # Process renewables data: Get latest year and clean columns
    ren = ren.rename(columns={"entity": "country"})
    year_cols = [c for c in ren.columns if c.isdigit()]
    latest_ren = ren[["country", year_cols[-1]]].rename(columns={year_cols[-1]: "renewables_share"})

    # Merge
    df = pd.merge(fos_latest, latest_ren, on="country", how="inner")
    return df, latest_year, year_cols[-1]

# Load data
df, fossil_year, renew_year = load_data()

st.title("Renewables Growth vs Fossil Reduction Correlation")
st.markdown("""
Scatter of countries’ **renewables share** vs their **fossil energy consumption** in the most recent year.
""")

fig = px.scatter(
    df,
    x="renewables_share",
    y="fossil_total",
    hover_name="country",
    title=f"Renewables Share vs Fossil Consumption ({fossil_year})",
    labels={
        "renewables_share": f"Renewables Share (% in {renew_year})",
        "fossil_total": "Fossil Energy Consumption (TWh)"
    }
)
fig.update_traces(marker=dict(size=10, color="green", line=dict(width=1, color="DarkSlateGrey")))
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown("""
    - This chart explores if countries with **higher renewable energy shares** tend to consume **less fossil fuel**.
    - Some countries like those in the EU show strong correlation, while others like China or India may still have high fossil use despite renewables growth.
    - A useful view to identify outliers or leaders in clean energy transition.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **Fossil data:** `owid-energy-data.xlsx`  (OWID)
    - **Renewables share:** `Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx`
    - **Latest Year Used:** Fossil = {fossil_year}, Renewables = {renew_year}
    """)
