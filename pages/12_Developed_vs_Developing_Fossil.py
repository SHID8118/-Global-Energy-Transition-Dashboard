# pages/12_Developed_vs_Developing_Fossil.py
"""
Dashboard: **Fossil‑fuel usage – Developed vs Developing (World Bank, Countries.csv)**

*Classification method*  (per World Bank data file `Countries.csv`)
- For each country, take the **latest available year** in `Countries.csv`.
- Use the column **`gdp per capita`** (already provided) to classify:
    * **Developed** ▶ GDP‑per‑capita ≥ 25 000 USD (2015 constant)
    * **Developing** ▶ below that threshold.

Metric plotted = `fossil_fuel_consumption` (TWh) from OWID.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Developed vs Developing – Fossil Trends", layout="wide", page_icon="🌐")

st.title("🌐 Fossil‑Fuel Consumption: Developed vs Developing (World Bank GDP‑per‑capita)")

# ──────────────────────────────────────────────────────────
# Load World Bank Countries.csv (user‑provided format)
# ──────────────────────────────────────────────────────────
@st.cache_data
def load_wb(path: str = "data/Countries.csv"):
    wb = pd.read_csv(path)
    wb.columns = wb.columns.str.strip().str.lower()
    wb = wb.rename(columns={"country name": "country", "country code": "iso_code"})
    # keep latest year per country
    wb_latest = wb.sort_values("year").groupby("iso_code").tail(1)
    wb_latest = wb_latest[["iso_code", "country", "gdp per capita"]].dropna()

    threshold = 25_000
    wb_latest["dev_status"] = wb_latest["gdp per capita"].apply(lambda x: "Developed" if x >= threshold else "Developing")
    return wb_latest

# ──────────────────────────────────────────────────────────
# Load OWID energy data
# ──────────────────────────────────────────────────────────
@st.cache_data
def load_owid(path: str = "data/owid-energy-data.xlsx"):
    ow = pd.read_excel(path)
    ow.columns = ow.columns.str.strip().str.lower()
    return ow

wb_df = load_wb()
owid_df = load_owid()

# merge on ISO code
merged = owid_df.merge(wb_df[["iso_code", "dev_status", "gdp per capita"]], on="iso_code", how="left")
merged = merged.dropna(subset=["dev_status", "fossil_fuel_consumption"])

# ──────────────────────────────────────────────────────────
# Aggregate developed vs developing trends
# ──────────────────────────────────────────────────────────
aggs = merged.groupby(["year", "dev_status"], as_index=False)["fossil_fuel_consumption"].sum()

min_y, max_y = int(aggs["year"].min()), int(aggs["year"].max())
start, end = st.slider("Select year range", min_y, max_y, (min_y, max_y))
agg_range = aggs[(aggs["year"] >= start) & (aggs["year"] <= end)]

fig = px.line(
    agg_range,
    x="year",
    y="fossil_fuel_consumption",
    color="dev_status",
    labels={"fossil_fuel_consumption": "Fossil Consumption (TWh)", "dev_status": "Group"},
    title=f"Fossil Consumption by Development Status ({start}–{end})",
    template="plotly_white"
)
fig.update_traces(mode="lines+markers")
st.plotly_chart(fig, use_container_width=True)

# Latest‑year country table
latest_yr = int(merged["year"].max())
latest_tbl = merged[merged["year"] == latest_yr][["country", "dev_status", "fossil_fuel_consumption", "gdp per capita"]]

with st.expander("🗺️ Country development status (latest year)"):
    st.dataframe(latest_tbl.sort_values("fossil_fuel_consumption", ascending=False).reset_index(drop=True))

with st.expander("📌 Insights"):
    st.markdown(
        """
        * Classification uses **World Bank GDP‑per‑capita threshold** of **$25k**.
        * Developed group shows stabilising or declining fossil use, while Developing continues to rise.
        * Use the year slider to examine historical divergence.
        """
    )

with st.expander("📊 Data Source"):
    st.markdown(
        """
        * **OWID energy dataset** – fossil_fuel_consumption (TWh)
        * **World Bank Countries.csv** – GDP per capita for development classification
        """
    )
