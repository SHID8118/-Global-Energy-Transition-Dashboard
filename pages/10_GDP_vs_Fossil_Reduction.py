# pages/10_GDP_vs_Fossil_Reduction.py
"""
Dashboard question:
**Which countries have reduced fossil fuel use while growing their GDP?**

Compares percentage‑change in real GDP versus percentage‑change in total fossil‑fuel
consumption (TWh) between the latest OWID year and 10 years earlier.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GDP ↑ vs Fossil ↓",
    layout="wide",
    page_icon="📈"
)

st.title("📈 Countries Growing GDP while Cutting Fossil Fuel Use")
st.markdown(
    """
    **Objective:** Identify economies that have **increased real GDP** while **reducing fossil‑fuel
    consumption** over the past decade.
    """
)

# ────────────────────────────────────────────────────────────────────────────────
# Data loader
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    cols_needed = ["country", "year", "gdp", "fossil_fuel_consumption"]
    missing = [c for c in cols_needed if c not in df.columns]
    if missing:
        st.error(f"Missing columns in dataset: {missing}")
        st.stop()

    latest_year = int(df["year"].max())
    base_year = latest_year - 10

    latest = df[df["year"] == latest_year][["country", "gdp", "fossil_fuel_consumption"]]
    base = df[df["year"] == base_year][["country", "gdp", "fossil_fuel_consumption"]]

    merged = (
        latest.merge(base, on="country", suffixes=("_latest", "_base"))
        .dropna(subset=["gdp_latest", "gdp_base", "fossil_fuel_consumption_latest", "fossil_fuel_consumption_base"])
    )

    merged["gdp_change_pct"] = (merged["gdp_latest"] - merged["gdp_base"]) / merged["gdp_base"] * 100
    merged["fossil_change_pct"] = (
        (merged["fossil_fuel_consumption_latest"] - merged["fossil_fuel_consumption_base"]) /
        merged["fossil_fuel_consumption_base"] * 100
    )
    return merged, base_year, latest_year

# Load
plot_df, base_year, latest_year = load_data()

# ────────────────────────────────────────────────────────────────────────────────
# Multiselect for focus countries
# ────────────────────────────────────────────────────────────────────────────────
all_countries = sorted(plot_df["country"].unique())
default_select = plot_df[(plot_df["gdp_change_pct"] > 0) & (plot_df["fossil_change_pct"] < 0)]["country"].head(8).tolist()
selected = st.multiselect("Highlight countries (optional):", all_countries, default_select)

highlight_df = plot_df[plot_df["country"].isin(selected)] if selected else plot_df

# ────────────────────────────────────────────────────────────────────────────────
# Scatter plot
# ────────────────────────────────────────────────────────────────────────────────
fig = px.scatter(
    highlight_df,
    x="gdp_change_pct",
    y="fossil_change_pct",
    hover_name="country",
    labels={"gdp_change_pct": "GDP change %", "fossil_change_pct": "Fossil‑fuel change %"},
    title=f"GDP Growth vs Fossil Reduction ({base_year} → {latest_year})",
    color="gdp_change_pct",
    template="plotly_white"
)
fig.add_shape(type="line", x0=0, x1=0, y0=plot_df["fossil_change_pct"].min(), y1=plot_df["fossil_change_pct"].max(), line=dict(dash="dash", color="grey"))
fig.add_shape(type="line", y0=0, y1=0, x0=plot_df["gdp_change_pct"].min(), x1=plot_df["gdp_change_pct"].max(), line=dict(dash="dash", color="grey"))
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────────
# Data table
# ────────────────────────────────────────────────────────────────────────────────
with st.expander("🔍 Full data"):
    st.dataframe(plot_df.sort_values(["gdp_change_pct"], ascending=False).reset_index(drop=True))

# ────────────────────────────────────────────────────────────────────────────────
# Insights & source
# ────────────────────────────────────────────────────────────────────────────────
with st.expander("📌 Key Insights"):
    st.markdown(
        f"""
        - **Quadrant analysis:**
          - **Upper‑left** (GDP ↑ / Fossil ↓) → successful decoupling.
          - **Lower‑right** (GDP ↓ / Fossil ↑) → undesirable trend.
        - Time range: **{base_year} → {latest_year}**.
        """
    )

with st.expander("📊 Data Source"):
    st.markdown(
        """
        - **Dataset:** `owid-energy-data.xlsx` – Our World in Data
        - **Variables:** `gdp`, `fossil_fuel_consumption`, `year`, `country`
        """
    )
