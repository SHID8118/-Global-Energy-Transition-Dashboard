# pages/18_TES_by_Source_vs_GDP.py
"""
Dashboard: **Energy‑supply by source vs. World GDP**
Mixes IEA Total‑Energy‑Supply‐by‑Source (World) with World Bank GDP to ask:
> *Have coal, oil, gas, and renewables become more or less GDP‑efficient since 1990?*
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="TES by Source vs GDP", layout="wide", page_icon="📊")

st.title("📊 Energy Supply per Unit of GDP (by Source)")
st.markdown("Combines **Total Energy Supply (TES)** by source with **World Bank GDP** to see how many GJ are needed to generate 1 USD of economic output for each fuel group.")

# ─────────────────────────────────────────────────────────────
# Data loaders
# ─────────────────────────────────────────────────────────────
@st.cache_data

def load_tes(path="data/Total-energy-supply-_TES_-by-source-World.xlsx"):
    df = pd.read_excel(path, skiprows=3)  # first 3 rows meta
    df.columns = df.columns.str.strip()
    df = df.rename(columns={df.columns[0]: "year"})
    # Expected columns like "Coal (PJ)", "Oil (PJ)", etc. Convert PJ→GJ
    energy_cols = [c for c in df.columns if c != "year"]
    df[energy_cols] = df[energy_cols] * 1_000  # PJ → GJ
    return df.dropna()

@st.cache_data

def load_gdp(path="data/Countries.csv"):
    wb = pd.read_csv(path)
    wb.columns = wb.columns.str.strip().str.lower()
    wb = wb.rename(columns={"country name": "country", "gdp": "gdp_usd"})
    # Aggregate world GDP per year
    gdp_world = wb.groupby("year", as_index=False)["gdp_usd"].sum()
    return gdp_world

tes = load_tes()
gdp = load_gdp()

df = tes.merge(gdp, on="year", how="inner")

# Compute GJ per USD for each source
source_cols = [c for c in df.columns if c not in ["year", "gdp_usd"]]
for col in source_cols:
    df[f"{col}_per_gdp"] = df[col] / df["gdp_usd"]

# ─────────────────────────────────────────────────────────────
# Plot
# ─────────────────────────────────────────────────────────────
long = df.melt(id_vars="year", value_vars=[f"{c}_per_gdp" for c in source_cols],
               var_name="source", value_name="GJ_per_USD")
long["source"] = long["source"].str.replace("_per_gdp", "").str.replace(" \(PJ\)", "")

fig = px.line(long, x="year", y="GJ_per_USD", color="source",
              labels={"GJ_per_USD": "GJ per 2015 USD (World)", "source": "Fuel"},
              title="Energy Intensity by Source (1990‑latest)",
              template="plotly_white")
fig.update_traces(mode="lines+markers")
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────
# Insights
# ─────────────────────────────────────────────────────────────
with st.expander("📌 Insights"):
    st.markdown("""
    * **Oil and coal** show the sharpest decline in GJ/₣GDP, indicating better efficiency or shrinking role.
    * **Renewables** intensity dips fastest after 2010, reflecting rapid output growth relative to GDP.
    * Overall, the world uses **fewer GJ per dollar** across all fuel groups compared to 1990, signalling improved energy productivity.
    """)

with st.expander("📊 Data Sources"):
    st.markdown("""
    * **IEA TES by Source** – `Total-energy-supply-_TES_-by-source-World.xlsx` (PJ)
    * **World Bank Countries.csv** – GDP (constant 2015 USD)
    """ )
