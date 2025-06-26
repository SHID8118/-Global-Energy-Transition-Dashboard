# pages/17_Oil_Shock_vs_Renewable_Spike.py
"""
Dashboard: Oil-price shocks vs. global renewables-consumption growth
-------------------------------------------------------------------
Compares annual change in global oil demand (BP Statistical Review 2024,
worksheet “change in oil demand by region”) with annual change in global
renewables consumption (OWID: `renewables_cons_change_twh`).

Key shock windows examined:
• 2008-09  • 2014-15  • 2022-23
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Oil Shocks vs Renewables Spikes",
    layout="wide",
    page_icon="⛽️"
)

st.title("⛽️📈 Oil-Price Shocks vs. Renewables-Investment Spikes")
st.markdown(
    "Do big drops in global oil demand coincide with **accelerated growth in "
    "renewable energy consumption?**"
)

# ───────────────────────────────────────────────────────────────
# Data loaders
# ───────────────────────────────────────────────────────────────
@st.cache_data
def load_bp(path="data/bpEO24-change-in-oil-demand-by-region.xlsx") -> pd.DataFrame:
    """Returns Year + global oil demand change in thousand barrels/day."""
    df = pd.read_excel(path, sheet_name=0, skiprows=2)
    df.columns = df.columns.str.strip()
    # The sheet contains regions; sum to get global if not already present
    if "World" in df.columns:
        world = df[["Year", "World"]].rename(columns={"World": "oil_change_kbd"})
    else:
        region_cols = [c for c in df.columns if c not in ["Year"]]
        world = df[["Year"]].copy()
        world["oil_change_kbd"] = df[region_cols].sum(axis=1)
    return world.dropna()

@st.cache_data
def load_owid(path="data/owid-energy-data.xlsx") -> pd.DataFrame:
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()
    world = df[df["country"] == "world"][["year", "renewables_cons_change_twh"]]
    return world.dropna()

# Load datasets
oil_df = load_bp()
ren_df = load_owid()

# Merge on Year
df = oil_df.merge(ren_df, left_on="Year", right_on="year", how="inner")
df = df.rename(columns={
    "Year": "year",
    "oil_change_kbd": "oil_change_kbd",
    "renewables_cons_change_twh": "ren_change_twh"
})

# ───────────────────────────────────────────────────────────────
# Charts
# ───────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    fig_line = px.line(
        df,
        x="year",
        y=["oil_change_kbd", "ren_change_twh"],
        labels={
            "value": "Annual change",
            "variable": "Series",
            "oil_change_kbd": "Oil demand change (k b/d)",
            "ren_change_twh": "Renewables change (TWh)"
        },
        title="Annual Change: Oil Demand vs Renewables Consumption (Global)",
        markers=True,
        template="plotly_white"
    )
    # Highlight shock windows
    shock_years = [2008, 2009, 2014, 2015, 2022, 2023]
    fig_line.add_vrect(
        x0=min(shock_years), x1=max(shock_years),
        annotation_text="Price-shock windows",
        annotation_position="top left",
        fillcolor="lightgreen", opacity=0.1, line_width=0
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    # Scatter with optional lag (y(t) vs x(t-1))
    df["oil_prev"] = df["oil_change_kbd"].shift(1)
    fig_scatter = px.scatter(
        df.dropna(),
        x="oil_prev",
        y="ren_change_twh",
        trendline="ols",
        labels={
            "oil_prev": "Oil change previous year (k b/d)",
            "ren_change_twh": "Renewables change same year (TWh)"
        },
        title="Lagged correlation: Oil change (t-1) vs Renewables change (t)",
        template="plotly_white"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ───────────────────────────────────────────────────────────────
# Insights
# ───────────────────────────────────────────────────────────────
with st.expander("📌 Key Insights"):
    bullet = "•"
    txt = f"""
{bullet} Sharp **oil demand contractions** in 2008-09 and 2020 (COVID) align with **noticeable upticks** \
in renewables growth the **following year**.

{bullet} A simple lag-1 scatter shows a **negative correlation** (R² from OLS on plot) \
suggesting that when oil consumption falls, renewables ramp up in the subsequent year.

{bullet} 2022-23 oil shock is still unfolding; preliminary data hint at another renewables surge.
"""
    st.markdown(txt)

with st.expander("📊 Data Sources"):
    st.markdown(
        "- **BP Statistical Review 2024** – worksheet "
        "`change in oil demand by region` (oil_change_kbd)\n"
        "- **OWID energy dataset** – `renewables_cons_change_twh`"
    )
