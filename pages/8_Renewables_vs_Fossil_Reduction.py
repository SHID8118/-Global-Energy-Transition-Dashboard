# pages/8_Renewables_vs_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(layout="wide", page_title="Ren vs Fossil Correlation", page_icon="🔗")

st.title("🔗 Renewables Growth vs Fossil Reduction Correlation")
st.markdown("""
This dashboard visualizes the correlation between countries' **modern renewable energy share** and their **fossil fuel consumption**.
A negative trend suggests a transition away from fossil fuels.
""")

@st.cache_data
def load_data():
    # Load fossil energy data
    fos = pd.read_excel("data/owid-energy-data.xlsx")

    # Ensure required columns exist
    fos_cols = ["country", "year", "coal_consumption", "oil_consumption", "gas_consumption"]
    fos = fos[[col for col in fos_cols if col in fos.columns]]
    fos = fos[fos["year"] == fos["year"].max()]  # Latest year

    fos["fossil_total"] = fos[["coal_consumption", "oil_consumption", "gas_consumption"]].sum(axis=1, skipna=True)
    fos = fos[["country", "fossil_total"]]

    # Load renewable share data
    ren = pd.read_excel("data/Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx", skiprows=3)
    ren.columns = ren.columns.str.strip()
    if "entity" in ren.columns:
        ren = ren.rename(columns={"entity": "country"})
    elif "Country" in ren.columns:
        ren = ren.rename(columns={"Country": "country"})

    year_cols = [col for col in ren.columns if str(col).isdigit()]
    latest_year = max(map(int, year_cols))
    ren = ren[["country", str(latest_year)]]
    ren = ren.rename(columns={str(latest_year): "renewables_share"})

    # Merge datasets
    df = fos.merge(ren, on="country")
    df = df.dropna(subset=["fossil_total", "renewables_share"])
    return df

# Load and prepare data
df = load_data()

# Scatter Plot
fig = px.scatter(
    df,
    x="renewables_share",
    y="fossil_total",
    hover_name="country",
    title="Renewable Share vs Fossil Fuel Consumption (Latest Year)",
    labels={
        "renewables_share": "Renewable Share (%)",
        "fossil_total": "Fossil Fuel Consumption (TWh)"
    },
    color="renewables_share",
    size_max=60
)
fig.update_traces(marker=dict(size=12, opacity=0.6, line=dict(width=1, color="DarkSlateGrey")))
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown("""
    - This scatter plot helps examine whether countries with **higher renewable shares** also consume **less fossil fuel**.
    - A downward slope suggests **transition effectiveness**: cleaner nations are moving away from coal, oil, and gas.
    - Outliers may indicate countries that have high renewables but still large fossil dependence.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - `owid-energy-data.xlsx` for fossil fuel consumption data
    - `Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx` for renewable share
    - Latest year data from both sources used
    """)
