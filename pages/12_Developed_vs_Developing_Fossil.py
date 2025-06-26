# pages/12_Developed_vs_Developing_Fossil.py
"""
Dashboard: **Compare fossil‑fuel usage trends between developed vs developing nations**

Definition here (using OWID aggregates):
* **Developed**  → *High‑income countries*
* **Developing** → *Low‑income*, *Lower‑middle‑income*, *Upper‑middle‑income* countries

Metric: `fossil_fuel_consumption` (TWh)
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Developed vs Developing – Fossil Trends", layout="wide", page_icon="🌐")

st.title("🌐 Fossil‑Fuel Usage: Developed vs Developing Nations")

# ────────────────────────────────────────────────────────────────────────────────
# Data loader
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    if "fossil_fuel_consumption" not in df.columns:
        st.error("Column `fossil_fuel_consumption` not found in OWID dataset.")
        st.stop()

    # keep only aggregate income‑group rows we need
    groups = {
        "high-income countries": "Developed",
        "upper-middle-income countries": "Developing",
        "lower-middle-income countries": "Developing",
        "low-income countries": "Developing",
    }
    df = df[df["country"].str.lower().isin(groups.keys())]
    df["group"] = df["country"].str.lower().map(groups)
    df = df[["year", "group", "fossil_fuel_consumption"]]
    df = df.dropna()
    return df

# load
df = load_data()
min_year, max_year = int(df["year"].min()), int(df["year"].max())

# year range selector
yr1, yr2 = st.slider("Select year range", min_year, max_year, (min_year, max_year))
plot_df = df[(df["year"] >= yr1) & (df["year"] <= yr2)]

# line chart
fig = px.line(
    plot_df,
    x="year",
    y="fossil_fuel_consumption",
    color="group",
    labels={"fossil_fuel_consumption": "Fossil Fuel Consumption (TWh)", "year": "Year", "group": "Group"},
    title=f"Fossil‑Fuel Consumption – Developed vs Developing ({yr1}–{yr2})",
    template="plotly_white"
)
fig.update_traces(mode="lines+markers")
st.plotly_chart(fig, use_container_width=True)

# table
with st.expander("🔍 Underlying data"):
    st.dataframe(plot_df)

# insights
with st.expander("📌 Insights"):
    st.markdown(
        """
        * Developed economies show a **flatter or declining** fossil‑fuel trend in recent years,
          while developing groups continue to **rise**, reflecting growing energy demand.
        * Energy‑transition policies and economic growth stages drive these divergent patterns.
        """
    )

# source
with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset · variable: fossil_fuel_consumption · XLSX file")
