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
over the last decade, and lets you explore their full consumption trends.
""")

@st.cache_data
def compute_reductions():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    max_year = int(df["year"].max())
    start_year = max_year - 10
    df = df[df["year"].isin([start_year, max_year])]
    df["fossil_total"] = (
        df["coal_consumption"].fillna(0) +
        df["oil_consumption"].fillna(0) +
        df["gas_consumption"].fillna(0)
    )
    pivot = df.pivot(index="country", columns="year", values="fossil_total").dropna()
    pivot["change_pct"] = ((pivot[max_year] - pivot[start_year]) / pivot[start_year] * 100).round(2)
    result = pivot.reset_index().sort_values("change_pct")
    return result, start_year, max_year

reductions_df, start_year, max_year = compute_reductions()

if reductions_df.empty:
    st.error("Insufficient data to compute reductions.")
    st.stop()

# Show top 10
top_n = 10
top10 = reductions_df.head(top_n)
st.subheader(f"Top {top_n} Countries by % Reduction ({start_year} → {max_year})")
st.dataframe(
    top10.rename(columns={
        start_year: f"{start_year} (TWh)",
        max_year: f"{max_year} (TWh)",
        "change_pct": "Change (%)"
    })[[ "country", f"{start_year} (TWh)", f"{max_year} (TWh)", "Change (%)" ]]
)

# Dropdown for selecting countries to plot
all_countries = reductions_df["country"].tolist()
default_countries = top10["country"].tolist()
selected = st.multiselect(
    "Select countries to view full consumption trends:",
    options=all_countries,
    default=default_countries
)

# Load full time series
@st.cache_data
def load_trends(countries):
    df_full = pd.read_excel("data/owid-energy-data.xlsx")
    df_full.columns = df_full.columns.str.strip().str.lower()
    df_full = df_full[df_full["country"].isin(countries)]
    df_full["fossil_total"] = (
        df_full["coal_consumption"].fillna(0) +
        df_full["oil_consumption"].fillna(0) +
        df_full["gas_consumption"].fillna(0)
    )
    df_full = df_full.dropna(subset=["year", "fossil_total"])
    df_full["year"] = df_full["year"].astype(int)
    return df_full

trend_df = load_trends(selected)

if trend_df.empty:
    st.warning("No trend data available for the selected countries.")
else:
    fig = px.line(
        trend_df,
        x="year",
        y="fossil_total",
        color="country",
        title="Fossil Fuel Consumption Trends",
        labels={
            "year": "Year",
            "fossil_total": "Total Fossil Consumption (TWh)",
            "country": "Country"
        },
        markers=True
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Narrative"):
    st.markdown(f"""
    Between **{start_year}** and **{max_year}**, the countries listed above reduced their total fossil fuel consumption by the greatest percentages.
    Use the dropdown to explore the full historical trends for any selection of countries.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **File:** `data/owid-energy-data.xlsx`  
    - **Columns used:** `country`, `year`, `coal_consumption`, `oil_consumption`, `gas_consumption`  
    - Data provided by Our World in Data.
    """)
