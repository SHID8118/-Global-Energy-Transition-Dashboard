# pages/8_Renewables_vs_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Ren vs Fossil Correlation", page_icon="🔗")

@st.cache_data

def load_data():
    # Load data
    fos = pd.read_excel("data/owid-energy-data.xlsx")
    ren = pd.read_excel("data/Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx", skiprows=3)

    # Normalize columns for easier access
    fos.columns = fos.columns.str.strip().str.lower()
    ren.columns = ren.columns.str.strip().str.lower()

    # Filter for latest year for fossil data
    fossil_year = fos["year"].max()
    fos_latest = fos[fos["year"] == fossil_year][["country", "coal_consumption", "oil_consumption", "gas_consumption"]].copy()
    fos_latest["fossil_total"] = fos_latest[["coal_consumption", "oil_consumption", "gas_consumption"]].sum(axis=1)

    # Reshape renewable data
    year_cols = [c for c in ren.columns if c.isdigit()]
    if not year_cols:
        st.error("No year columns found in renewable dataset")
        st.stop()

    latest_year = sorted(year_cols)[-1]  # use last year
    ren_latest = ren[["entity", latest_year]].rename(columns={"entity": "country", latest_year: "renewables_share"})

    # Merge
    merged = pd.merge(fos_latest, ren_latest, on="country")
    merged = merged.dropna(subset=["renewables_share", "fossil_total"])
    return merged, fossil_year, latest_year

# Load and prepare data
df, fossil_year, ren_year = load_data()

# Title and Description
st.title("🔗 Renewable Share vs Fossil Consumption")
st.markdown(f"""
This dashboard shows a **scatter plot** comparing the **renewables share** (SDG 7.2) to total **fossil fuel consumption**.
It highlights how countries are transitioning from fossil fuels to clean energy.

- **Renewables Share Year:** {ren_year}
- **Fossil Data Year:** {fossil_year}
""")

# Scatter Plot
fig = px.scatter(
    df,
    x="renewables_share",
    y="fossil_total",
    hover_name="country",
    labels={"renewables_share": "Renewable Share (%)", "fossil_total": "Fossil Consumption (TWh)"},
    title="Renewables Share vs Fossil Fuel Consumption"
)
fig.update_traces(marker=dict(size=10, color='green'))
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown("""
    - Countries with **higher renewable shares** often exhibit **lower fossil fuel consumption**, but the correlation is not absolute.
    - Outliers may reflect **large economies** with high consumption but increasing renewables.
    - The relationship provides a lens into **energy transition progress**.
    """)

# Data Source
with st.expander("📊 Data Sources"):
    st.markdown("""
    - `owid-energy-data.xlsx` (coal, oil, gas consumption by country)
    - `Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx` (SDG 7.2 share)
    """)
