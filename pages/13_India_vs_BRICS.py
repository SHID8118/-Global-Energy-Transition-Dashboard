# pages/13_India_vs_BRICS.py
"""
Dashboard: **How does India compare to other BRICS nations in reducing fossil‑fuel use?**

*BRICS countries*: **Brazil, Russia, India, China, South Africa**
Metric analysed = `fossil_fuel_consumption` (TWh) from OWID.
We look at both the absolute trajectory (2000‑latest) and the **10‑year % change**.
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
    df = df[df["country"].isin([c.lower() for c in BRICS])]
    return df

df = load_owid()

# Make country names proper case again
name_map = {c.lower(): c for c in BRICS}
df["country"] = df["country"].map(name_map)

# ────────────────────────────────────────────────────────────────────────────────
# Line chart – fossil consumption over time
# ────────────────────────────────────────────────────────────────────────────────
line_df = df.dropna(subset=["fossil_fuel_consumption"])
fig_line = px.line(
    line_df,
    x="year",
    y="fossil_fuel_consumption",
    color="country",
    labels={"fossil_fuel_consumption": "Fossil Consumption (TWh)", "country": "Country"},
    title="Fossil‑Fuel Consumption Trajectory (2000‑Latest)",
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

# Bar chart – % change
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
fig_bar.update_layout(xaxis_title="Country", yaxis_title="% Change")
fig_bar.add_hline(y=0, line_dash="dash", line_color="grey")
st.plotly_chart(fig_bar, use_container_width=True)

# ────────────────────────────────────────────────────────────────────────────────
# Insights & data source
# ────────────────────────────────────────────────────────────────────────────────
with st.expander("📌 Insights"):
    st.markdown(
        f"""
        * **India** shows a **{{change_df.loc[change_df.country=='India','pct_change'].values[0]:.1f}} %** change over the last decade.
        * Positive bars indicate growth in fossil use, negative bars show reduction.
        * Examine the line chart to see long‑term trajectories since 2000.
        """
    )

with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset – variable: `fossil_fuel_consumption` (TWh)")
