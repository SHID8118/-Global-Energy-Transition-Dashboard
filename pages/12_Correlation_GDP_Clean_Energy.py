# pages/11_Correlation_GDP_Clean_Energy.py
"""
Dashboard: **Is there a correlation between GDP growth and clean‑energy investment?**

Proxy for “clean‑energy investment”  → change in **renewables_consumption** (TWh) over the
same period we measure GDP growth.  Positive correlation suggests economies are
investing in renewables while expanding economically.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import pearsonr

# ────────────────────────────────────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="GDP vs Clean‑Energy Correlation", layout="wide", page_icon="🔗")

st.title("🔗 Correlation between GDP Growth and Clean‑Energy Investment")

st.markdown(
    """
    **Clean‑energy investment proxy**  → growth in *renewables consumption* (TWh).
    We compare 10‑year percentage changes in GDP and renewables consumption for each
    country using OWID data.
    """
)

# ────────────────────────────────────────────────────────────────────────────────
# Data loader
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    needed = ["country", "year", "gdp", "renewables_consumption"]
    if any(col not in df.columns for col in needed):
        st.error("Dataset missing required columns (gdp / renewables_consumption).")
        st.stop()

    df = df.dropna(subset=["gdp", "renewables_consumption"])

    latest_year = int(df["year"].max())

    # choose base year 10y earlier if overlap exists else 5y earlier
    for offset in (10, 5):
        base_year = latest_year - offset
        common = set(df[df["year"] == latest_year]["country"]).intersection(
            df[df["year"] == base_year]["country"])
        if len(common) >= 30:
            break
    else:
        st.error("Insufficient overlap to compute 5‑ or 10‑year change.")
        st.stop()

    latest = df[df["year"] == latest_year][["country", "gdp", "renewables_consumption"]]
    base = df[df["year"] == base_year][["country", "gdp", "renewables_consumption"]]

    merged = (
        latest.merge(base, on="country", suffixes=("_latest", "_base"))
        .assign(
            gdp_change_pct=lambda d: (d["gdp_latest"] - d["gdp_base"]) / d["gdp_base"] * 100,
            ren_change_pct=lambda d: (d["renewables_consumption_latest"] - d["renewables_consumption_base"]) / d["renewables_consumption_base"] * 100,
        )
        .dropna(subset=["gdp_change_pct", "ren_change_pct"])
    )
    return merged, base_year, latest_year

# load data
plot_df, base_year, latest_year = load_data()

# correlation coefficient
corr_val, p_val = pearsonr(plot_df["gdp_change_pct"], plot_df["ren_change_pct"])

# multiselect highlight
all_countries = sorted(plot_df["country"].unique())
highlight = st.multiselect("Highlight countries (optional):", all_countries)
h_df = plot_df if not highlight else plot_df[plot_df["country"].isin(highlight)]

# scatter plot
fig = px.scatter(
    h_df,
    x="gdp_change_pct",
    y="ren_change_pct",
    hover_name="country",
    labels={"gdp_change_pct": "GDP change %", "ren_change_pct": "Renewables consumption change %"},
    title=f"GDP Growth vs Renewables Growth  ( {base_year} → {latest_year} )\nPearson r = {corr_val:.2f} (p={p_val:.3f})",
    color="gdp_change_pct",
    template="plotly_white"
)
fig.add_vline(x=0, line_dash="dash", line_color="grey")
fig.add_hline(y=0, line_dash="dash", line_color="grey")
fig.update_layout(hovermode="closest")

st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 Full data"):
    st.dataframe(plot_df.sort_values("gdp_change_pct", ascending=False))

with st.expander("📌 Insights"):
    trend = "positive" if corr_val > 0 else "negative"
    st.markdown(
        f"Pearson correlation (r) between **GDP growth** and **renewables growth** is **{corr_val:.2f}** → {trend} relationship."  # noqa: E501
    )

with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset · variables: gdp, renewables_consumption · XLSX file")
