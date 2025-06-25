# pages/1_Countries_Reducing_Fossil_Consumption.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Top Fossil Reducers",
    layout="wide",
    page_icon="📉"
)

st.title("📉 Countries Reducing Fossil Fuel Consumption the Most (Last Decade)")
st.markdown("""
This dashboard identifies which countries have achieved the largest **percentage reduction** in total fossil fuel consumption (coal + oil + gas)
over the last decade.
""")

@st.cache_data
def load_data():
    # Load OWID energy data
    df = pd.read_excel("data/owid-energy-data.xlsx")
    # Clean column names
    df.columns = df.columns.str.strip().str.lower()
    # Filter relevant years
    max_year = int(df["year"].max())
    start_year = max_year - 10
    df = df[df["year"].isin([start_year, max_year])]
    # Compute total fossil consumption
    df["fossil_total"] = (
        df.get("coal_consumption", 0).fillna(0) +
        df.get("oil_consumption", 0).fillna(0) +
        df.get("gas_consumption", 0).fillna(0)
    )
    # Pivot so each country has start and end values
    pivot = df.pivot_table(
        index="country",
        columns="year",
        values="fossil_total"
    ).dropna()
    pivot["change_pct"] = ((pivot[max_year] - pivot[start_year]) / pivot[start_year] * 100).round(2)
    # Sort by largest negative change (biggest reduction)
    result = pivot.sort_values("change_pct").reset_index()
    return result, start_year, max_year

df_change, start_year, max_year = load_data()

if df_change.empty:
    st.warning("No data available for the selected period. Please check your data source.")
    st.stop()

# Show top 10 reducers
top_n = 10
st.subheader(f"Top {top_n} Countries by % Reduction in Fossil Fuel Use ({start_year} → {max_year})")
st.dataframe(df_change[["country", start_year, max_year, "change_pct"]].head(top_n).rename(columns={
    start_year: f"{start_year} (TWh)",
    max_year: f"{max_year} (TWh)",
    "change_pct": "Change (%)"
}))

# Plot trends for top 5
top5 = df_change.head(5)["country"].tolist()
trend_df = pd.read_excel("data/owid-energy-data.xlsx")
trend_df = trend_df[trend_df["country"].isin(top5)]
trend_df["fossil_total"] = (
    trend_df.get("coal_consumption", 0).fillna(0) +
    trend_df.get("oil_consumption", 0).fillna(0) +
    trend_df.get("gas_consumption", 0).fillna(0)
)

fig = px.line(
    trend_df,
    x="year",
    y="fossil_total",
    color="country",
    title="Fossil Fuel Consumption Trend for Top 5 Reducers",
    labels={"year":"Year", "fossil_total":"Total Fossil Consumption (TWh)", "country":"Country"},
    markers=True
)
fig.update_layout(legend_title_text="Country")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Narrative"):
    st.markdown(f"""
    Over the period **{start_year} to {max_year}**, the following countries achieved the largest percentage cuts in 
    coal, oil, and gas consumption, indicating strong progress in their energy transition:
    - **{', '.join(top5)}** lead the list of top reducers.
    - These declines reflect shifts to renewables, efficiency measures, and policy interventions.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **File:** `data/owid-energy-data.xlsx`  
    - **Columns used:** `country`, `year`, `coal_consumption`, `oil_consumption`, `gas_consumption`  
    - Data provided by Our World in Data.
    """)
