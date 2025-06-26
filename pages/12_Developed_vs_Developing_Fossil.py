# pages/12_Developed_vs_Developing_Fossil.py
"""
Dashboard: **Compare fossil‑fuel usage trends between developed vs developing nations**

### Two perspectives
1. **Income‑group aggregates** (OWID rows: High‑income, Upper‑/Lower‑middle, Low‑income).
2. **Country‑level classification**  – we flag each country *Developed* vs *Developing* using a simple
   GDP‑per‑capita threshold (\$25 000 constant‑2015 USD).

Metric visualised = **`fossil_fuel_consumption` (TWh)**.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────────────────────────────────────
# Config
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Developed vs Developing – Fossil Trends", layout="wide", page_icon="🌐")

st.title("🌐 Fossil‑Fuel Consumption: Developed vs Developing Nations")

# ----------------------------------------------------------------------------
# Load OWID data
# ----------------------------------------------------------------------------
@st.cache_data

def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    req = ["country", "year", "fossil_fuel_consumption", "gdp", "population"]
    if any(c not in df.columns for c in req):
        st.error("Dataset missing columns needed: fossil_fuel_consumption, gdp, population.")
        st.stop()

    return df

df_full = load_data()

# ----------------------------------------------------------------------------
# Aggregate income‑group rows (Developed vs Developing)
# ----------------------------------------------------------------------------
agg_map = {
    "high-income countries": "Developed",
    "upper-middle-income countries": "Developing",
    "lower-middle-income countries": "Developing",
    "low-income countries": "Developing",
}
agg_df = df_full[df_full["country"].str.lower().isin(agg_map.keys())].copy()
agg_df["group"] = agg_df["country"].str.lower().map(agg_map)
agg_df = agg_df[["year", "group", "fossil_fuel_consumption"]].dropna()

# ----------------------------------------------------------------------------
# YEAR RANGE slider for aggregates
# ----------------------------------------------------------------------------
min_y, max_y = int(agg_df["year"].min()), int(agg_df["year"].max())
start, end = st.slider("Select year range (aggregates)", min_y, max_y, (min_y, max_y))
range_df = agg_df[(agg_df["year"] >= start) & (agg_df["year"] <= end)]

# ----------------------------------------------------------------------------
# Aggregate line chart
# ----------------------------------------------------------------------------
fig = px.line(
    range_df,
    x="year",
    y="fossil_fuel_consumption",
    color="group",
    labels={"fossil_fuel_consumption": "Fossil Consumption (TWh)", "group": "Group"},
    title=f"Aggregate Fossil‑Fuel Consumption ({start}–{end})",
    template="plotly_white"
)
fig.update_traces(mode="lines+markers")
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------
# Country‑level classification by GDP‑per‑capita
# ----------------------------------------------------------------------------
latest_year = int(df_full["year"].max())
country_latest = df_full[df_full["year"] == latest_year].copy()
country_latest = country_latest.dropna(subset=["gdp", "population", "fossil_fuel_consumption"])
country_latest["gdp_pc"] = country_latest["gdp"] / country_latest["population"]
threshold = 25_000  # USD 2015 constant
country_latest["dev_status"] = country_latest["gdp_pc"].apply(lambda x: "Developed" if x >= threshold else "Developing")

# top‑n slider & bar chart of country efficiency
st.subheader(f"{latest_year}: Country Fossil Consumption by Development Status")
N = st.slider("Top N countries", 5, 30, 15)
bar_df = (
    country_latest.sort_values("fossil_fuel_consumption", ascending=False)
    .head(N)
)
fig2 = px.bar(
    bar_df,
    x="country",
    y="fossil_fuel_consumption",
    color="dev_status",
    labels={"fossil_fuel_consumption": "Fossil Consumption (TWh)", "country": "Country", "dev_status": "Status"},
    title=f"Top {N} Fossil Consumers – {latest_year} (colour by development status)",
    template="plotly_white"
)
fig2.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------------------------------------------------
# Mapping tables
# ----------------------------------------------------------------------------
with st.expander("🗺️ Income‑group aggregates used"):
    st.dataframe(pd.DataFrame({
        "OWID Aggregate": list(agg_map.keys()),
        "Category": list(agg_map.values())
    }))

with st.expander("🗺️ Country‑level classification (latest year)"):
    st.dataframe(country_latest[["country", "dev_status", "gdp_pc"]].sort_values("gdp_pc", ascending=False))

# ----------------------------------------------------------------------------
# Insights & source
# ----------------------------------------------------------------------------
with st.expander("📌 Insights"):
    st.markdown(
        """
        * Aggregate view shows **Developing** economies’ fossil‑fuel demand still rising, while
          **Developed** plateaus or declines.
        * Country‑level view shows the dominance of large developing economies in absolute fossil
          usage, but some high‑income nations remain major consumers.
        """
    )

with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset · variables: fossil_fuel_consumption, gdp, population")
