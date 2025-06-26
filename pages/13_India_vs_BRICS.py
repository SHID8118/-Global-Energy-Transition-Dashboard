# pages/13_India_vs_BRICS.py
"""
Dashboard: **How does India compare to other BRICS nations in reducing fossil‑fuel use?**

BRICS = Brazil, Russia, India, China, South Africa.
Metric → `fossil_fuel_consumption` (TWh) from OWID.

Fixes:
* Ensure case‑insensitive country filtering (`str.lower()`).
* Handle missing base‑year rows gracefully.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="India vs BRICS – Fossil Trends", layout="wide", page_icon="🇮🇳")

st.title("🇮🇳 India vs Other BRICS Countries – Fossil‑Fuel Reduction")

BRICS = ["Brazil", "Russia", "India", "China", "South Africa"]

# ────────────────────────────────────────────────────────────────────────────────
# Load OWID data
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_owid(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()
    # keep only BRICS rows (case‑insensitive)
    df = df[df["country"].str.lower().isin([c.lower() for c in BRICS])]
    return df

df = load_owid()

# Map original capitalisation back
name_map = {c.lower(): c for c in BRICS}
df["country"] = df["country"].map(name_map)

# Abort if data missing
if df.empty:
    st.error("No BRICS data found in OWID file – check country names.")
    st.stop()

# ────────────────────────────────────────────────────────────────────────────────
# Line chart since 2000
# ────────────────────────────────────────────────────────────────────────────────
line_df = df.dropna(subset=["fossil_fuel_consumption"])
fig_line = px.line(
    line_df,
    x="year",
    y="fossil_fuel_consumption",
    color="country",
    labels={"fossil_fuel_consumption": "Fossil Consumption (TWh)", "country": "Country"},
    title="Fossil‑Fuel Consumption Trajectory (2000‑latest)",
    template="plotly_white"
)
fig_line.update_traces(mode="lines+markers")
st.plotly_chart(fig_line, use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────────
# 10‑year % change comparison
# ────────────────────────────────────────────────────────────────────────────────
latest_year = int(df["year"].max())
base_year = latest_year - 10

latest = df[df["year"] == latest_year][["country", "fossil_fuel_consumption"]].rename(columns={"fossil_fuel_consumption": "latest"})
base = df[df["year"] == base_year][["country", "fossil_fuel_consumption"]].rename(columns={"fossil_fuel_consumption": "base"})

change_df = latest.merge(base, on="country", how="inner")
change_df["pct_change"] = (change_df["latest"] - change_df["base"]) / change_df["base"] * 100

fig_bar = px.bar(
    change_df,
    x="country",
    y="pct_change",
    labels={"pct_change": "% Change (last 10 years)"},
    color="pct_change",
    color_continuous_scale="RdYlGn_r",
    title=f"10‑Year Change in Fossil‑Fuel Consumption ({base_year}→{latest_year})",
    template="plotly_white"
)
fig_bar.add_hline(y=0, line_dash="dash", line_color="grey")
fig_bar.update_layout(xaxis_title="Country", yaxis_title="% Change")
st.plotly_chart(fig_bar, use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────────
# Insights & data source
# ────────────────────────────────────────────────────────────────────────────────
with st.expander("📌 Insights"):
    india_pct = change_df.loc[change_df.country == "India", "pct_change"].values
    india_msg = f"India's 10‑year change: **{india_pct[0]:.1f}%**." if len(india_pct) else "India has insufficient data for 10‑year comparison."
    st.markdown(india_msg)

with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset – variable: `fossil_fuel_consumption` (TWh)")
