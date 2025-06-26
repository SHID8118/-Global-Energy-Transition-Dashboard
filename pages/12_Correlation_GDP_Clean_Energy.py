# pages/12_Correlation_GDP_Clean_Energy.py
"""
Dashboard: **Is there a correlation between GDP growth and clean‑energy investment?**

*Clean‑energy investment proxy* → % change in **renewables_consumption** (TWh).
We compare 10‑year percentage changes for GDP and renewables per country
(using OWID data) and compute the Pearson *r* with **pandas** only (no SciPy).
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="GDP vs Clean Energy", layout="wide", page_icon="🔗")

st.title("🔗 GDP Growth vs Clean‑Energy Investment")

st.markdown(
    """
    **Method**: For each country, compute 10‑year % change in real GDP and in
    *renewables consumption*. Scatter the two and report Pearson correlation.
    """
)

# ────────────────────────────────────────────────────────────────────────────────
# Data loader
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    req = ["country", "year", "gdp", "renewables_consumption"]
    if any(c not in df.columns for c in req):
        st.error("Required columns missing in dataset: gdp / renewables_consumption.")
        st.stop()

    df = df.dropna(subset=["gdp", "renewables_consumption"])
    latest_year = int(df["year"].max())

    # pick a base year with overlap (10→5 year fallback)
    base_year = None
    for off in (10, 5):
        y = latest_year - off
        overlap = set(df[df["year"] == latest_year]["country"]).intersection(df[df["year"] == y]["country"])
        if len(overlap) >= 30:
            base_year = y
            break
    if base_year is None:
        st.error("No sufficient overlap for 10‑/5‑year comparison.")
        st.stop()

    lat = df[df["year"] == latest_year][["country", "gdp", "renewables_consumption"]]
    bas = df[df["year"] == base_year][["country", "gdp", "renewables_consumption"]]

    merged = (
        lat.merge(bas, on="country", suffixes=("_latest", "_base"))
        .assign(
            gdp_change_pct=lambda d: (d["gdp_latest"] - d["gdp_base"]) / d["gdp_base"] * 100,
            ren_change_pct=lambda d: (d["renewables_consumption_latest"] - d["renewables_consumption_base"]) / d["renewables_consumption_base"] * 100,
        )
        .dropna(subset=["gdp_change_pct", "ren_change_pct"])
    )
    return merged, base_year, latest_year

# Load
df, base_y, lat_y = load_data()

# Pearson correlation via pandas
corr_val = df[["gdp_change_pct", "ren_change_pct"]].corr().iloc[0, 1]
trend = "positive" if corr_val > 0 else "negative"

# Multiselect
countries = sorted(df["country"].unique())
highlight = st.multiselect("Highlight countries (optional):", countries)
show_df = df if not highlight else df[df["country"].isin(highlight)]

# Scatter
fig = px.scatter(
    show_df,
    x="gdp_change_pct",
    y="ren_change_pct",
    hover_name="country",
    labels={"gdp_change_pct": "GDP change %", "ren_change_pct": "Renewables consumption change %"},
    title=f"GDP vs Renewables Growth  ( {base_y} → {lat_y} ) — Pearson r = {corr_val:.2f} ({trend})",
    color="gdp_change_pct",
    template="plotly_white"
)
fig.add_vline(x=0, line_dash="dash", line_color="grey")
fig.add_hline(y=0, line_dash="dash", line_color="grey")
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

# Full table
with st.expander("🔍 Full table"):
    st.dataframe(df.sort_values("gdp_change_pct", ascending=False))

# Insights
with st.expander("📌 Insights"):
    st.markdown(
        f"Pearson **r = {corr_val:.2f}** between GDP growth and renewables growth over {base_y}→{lat_y}."
    )

# Data source
with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset · variables: gdp, renewables_consumption · XLSX file")
