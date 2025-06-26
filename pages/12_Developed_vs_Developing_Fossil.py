# pages/12_Developed_vs_Developing_Fossil.py
"""
Dashboard: **Compare fossil‑fuel usage trends between developed vs developing nations**

Group definition (OWID income aggregates):
* **Developed**   → `High‑income countries`
* **Developing** → `Upper‑middle`, `Lower‑middle`, `Low‑income` country groups

Metric: `fossil_fuel_consumption` (TWh)
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Developed vs Developing – Fossil Trends", layout="wide", page_icon="🌐")

st.title("🌐 Fossil‑Fuel Consumption: Developed vs Developing Nations")

# ────────────────────────────────────────────────────────────────────────────────
# Data loader
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    if "fossil_fuel_consumption" not in df.columns:
        st.error("Column `fossil_fuel_consumption` not found in dataset.")
        st.stop()

    groups_map = {
        "high-income countries": "Developed",
        "upper-middle-income countries": "Developing",
        "lower-middle-income countries": "Developing",
        "low-income countries": "Developing",
    }

    df = df[df["country"].str.lower().isin(groups_map.keys())].copy()
    df["group"] = df["country"].str.lower().map(groups_map)
    df = df[["year", "group", "fossil_fuel_consumption"]]
    df = df.dropna()

    # Make mapping table for display
    mapping_tbl = pd.DataFrame({
        "OWID Aggregate": list(groups_map.keys()),
        "Category": list(groups_map.values())
    })
    return df, mapping_tbl

# Load data
plot_df, mapping_df = load_data()
min_year, max_year = int(plot_df["year"].min()), int(plot_df["year"].max())

# Year slider
start, end = st.slider("Select year range:", min_year, max_year, (min_year, max_year))
range_df = plot_df[(plot_df["year"] >= start) & (plot_df["year"] <= end)]

# Line chart
fig = px.line(
    range_df,
    x="year",
    y="fossil_fuel_consumption",
    color="group",
    labels={"fossil_fuel_consumption": "Fossil Fuel Consumption (TWh)", "year": "Year", "group": "Group"},
    title=f"Fossil‑Fuel Consumption ({start}–{end})",
    template="plotly_white"
)
fig.update_traces(mode="lines+markers")
st.plotly_chart(fig, use_container_width=True)

# Mapping table
with st.expander("🗺️ Country‑group mapping"):
    st.markdown("*OWID aggregate rows considered in this comparison.*")
    st.dataframe(mapping_df)

# Underlying data
with st.expander("🔍 Data used for chart"):
    st.dataframe(range_df)

# Insights
with st.expander("📌 Insights"):
    st.markdown(
        """
        * Developed economies show a **flattening or decline** in fossil consumption in recent
          years.
        * Developing groups continue a **growth trajectory**, reflecting industrialisation and
          rising energy demand.
        * Energy‑transition policies and economic structures drive these divergent paths.
        """
    )

# Source
with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset – variable: `fossil_fuel_consumption` (TWh)")
