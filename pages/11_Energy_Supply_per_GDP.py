# pages/10_Energy_Supply_per_GDP.py
"""
Dashboard: **Energy supply per unit GDP** – Which countries are the most energy‑efficient?
Metric in OWID = `energy_per_gdp` (kWh per *constant* 2015 USD GDP).
Lower values → higher efficiency.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────────────────────────────────────
# Page config
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Energy Intensity vs GDP",
    layout="wide",
    page_icon="⚡️"
)

st.title("⚡️ Energy Supply per Unit GDP (Energy Intensity)")
st.markdown(
    """
    **Energy intensity** is measured as total primary energy supply *per* unit of real GDP.
    Lower values indicate **greater energy efficiency**.
    """
)

# ────────────────────────────────────────────────────────────────────────────────
# Data loader
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    if "energy_per_gdp" not in df.columns:
        st.error("Column `energy_per_gdp` not found – ensure OWID data version includes this metric.")
        st.stop()

    latest_year = int(df[df["energy_per_gdp"].notna()]["year"].max())
    latest_df = df[(df["year"] == latest_year) & df["energy_per_gdp"].notna()][["country", "energy_per_gdp"]].copy()

    # remove aggregates
    aggregates = ["world", "asia", "europe", "north america", "south america", "africa", "european union", "oceania"]
    latest_df = latest_df[~latest_df["country"].str.lower().isin(aggregates)]

    latest_df = latest_df.sort_values("energy_per_gdp")  # lowest (best) first
    return latest_df, latest_year

# load
rank_df, year = load_data()

# top‑N slider
N = st.slider("Show top N most efficient countries", 5, 30, 15)
plot_df = rank_df.head(N)

# bar chart (lower is better)
fig = px.bar(
    plot_df,
    x="country",
    y="energy_per_gdp",
    title=f"Top {N} Energy‑Efficient Countries – {year}",
    labels={"energy_per_gdp": "Energy per GDP (kWh / 2015 USD)", "country": "Country"},
    color="energy_per_gdp",
    color_continuous_scale="Blues_r",  # reversed so darker = lower (better)
    height=550,
    template="plotly_white"
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# full table
with st.expander("🔍 Full table"):
    st.dataframe(rank_df.reset_index(drop=True))

# insights
with st.expander("📌 Insights"):
    st.markdown(
        f"""
        - Countries at the top (lowest bars) use **less energy per unit of economic output**, indicating **higher energy efficiency**.
        - Energy intensity depends on industrial structure, technology, and climate policies.
        - Metric year: **{year}**.
        """
    )

# data source
with st.expander("📊 Data Source"):
    st.markdown(
        """
        - **Dataset:** `owid-energy-data.xlsx` – Our World in Data
        - **Variable:** `energy_per_gdp`  (kWh per constant‑2015 USD GDP)
        - Lower value ⇒ more GDP produced per unit energy.
        """
    )
