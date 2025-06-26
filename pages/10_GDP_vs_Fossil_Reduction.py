# pages/10_GDP_vs_Fossil_Reduction.py
"""
Dashboard: **Which countries have reduced fossil fuel use while growing GDP?**

Logic tweak
-----------
* Find the **latest year** in OWID data that has *both* `gdp` and
  `fossil_fuel_consumption` for ≥ 1 country (often 2022).
* Work **backwards** up to 10 years; choose the earliest year within that
  window that still has complete data for the same countries.
* Calculate %‑change (GDP ↑ vs Fossils ↓).
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="GDP ↑ vs Fossil ↓", layout="wide", page_icon="📈")

st.title("📈 Countries Growing GDP while Cutting Fossil-Fuel Use")

@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    required = ["country", "year", "gdp", "fossil_fuel_consumption"]
    if any(c not in df.columns for c in required):
        st.error("Dataset missing required columns.")
        st.stop()

    # keep only rows with both metrics
    df = df.dropna(subset=["gdp", "fossil_fuel_consumption"])

    latest_year = int(df["year"].max())

    # search for a base year 5‑10 years back with enough overlap
    base_year = None
    for offset in range(10, 4, -1):  # 10→5
        cand = latest_year - offset
        common = set(df[df["year"] == latest_year]["country"]).intersection(
            df[df["year"] == cand]["country"]
        )
        if len(common) >= 30:  # arbitrary threshold for meaningful sample
            base_year = cand
            break

    if base_year is None:
        st.error("Could not find a suitable base year with overlapping data.")
        st.stop()

    latest = df[df["year"] == latest_year][["country", "gdp", "fossil_fuel_consumption"]]
    base = df[df["year"] == base_year][["country", "gdp", "fossil_fuel_consumption"]]

    merged = (
        latest.merge(base, on="country", how="inner", suffixes=("_latest", "_base"))
        .assign(
            gdp_change_pct=lambda d: (d["gdp_latest"] - d["gdp_base"]) / d["gdp_base"] * 100,
            fossil_change_pct=lambda d: (d["fossil_fuel_consumption_latest"] - d["fossil_fuel_consumption_base"]) / d["fossil_fuel_consumption_base"] * 100,
        )
    )
    return merged, base_year, latest_year

# load
plot_df, base_year, latest_year = load_data()

# multiselect
countries = sorted(plot_df["country"].unique())
select = st.multiselect("Highlight countries (optional):", countries)
show_df = plot_df if not select else plot_df[plot_df["country"].isin(select)]

# scatter
fig = px.scatter(
    show_df,
    x="gdp_change_pct",
    y="fossil_change_pct",
    hover_name="country",
    title=f"GDP change vs Fossil change  ( {base_year} → {latest_year} )",
    labels={"gdp_change_pct": "GDP change %", "fossil_change_pct": "Fossil‑fuel change %"},
    color="gdp_change_pct",
    template="plotly_white"
)
fig.add_vline(x=0, line_dash="dash", line_color="grey")
fig.add_hline(y=0, line_dash="dash", line_color="grey")
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 Full table"):
    st.dataframe(plot_df.sort_values("gdp_change_pct", ascending=False))

with st.expander("📌 Insights"):
    st.markdown(
        f"**Upper‑left quadrant**  → GDP ↑, Fossils ↓  → successful decoupling.\n"
        f"Period analysed: **{base_year}** → **{latest_year}**."
    )

with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset · variables: gdp, fossil_fuel_consumption · XLSX file")
