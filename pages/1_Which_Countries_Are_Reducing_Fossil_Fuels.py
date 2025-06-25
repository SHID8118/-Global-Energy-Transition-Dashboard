import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Fossil vs Renewables", page_icon="📉")

@st.cache_data
def load_data():
    # Load each source file and rename the generation column
    coal_df = (
        pd.read_excel("data/emberChartData.xlsx")[["Year", "generation_twh"]]
        .dropna()
        .rename(columns={"generation_twh": "Coal"})
    )
    gas_df = (
        pd.read_excel("data/emberChartData-_1_.xlsx")[["Year", "generation_twh"]]
        .dropna()
        .rename(columns={"generation_twh": "Gas"})
    )
    wind_df = (
        pd.read_excel("data/emberChartData-_2_.xlsx")[["Year", "generation_twh"]]
        .dropna()
        .rename(columns={"generation_twh": "Wind & Solar"})
    )

    # Merge on Year
    df = coal_df.merge(gas_df, on="Year", how="inner").merge(wind_df, on="Year", how="inner")
    df["Fossil Fuels"] = df["Coal"] + df["Gas"]
    return df

df = load_data()

# Header + Download
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📉 Global Fossil vs Renewable Energy Trends (2000–2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "fossil_vs_renewables.csv")

# Area Chart
fig = px.area(
    df,
    x="Year",
    y=["Fossil Fuels", "Wind & Solar"],
    title="Global Electricity Generation Mix",
    labels={"value": "TWh", "variable": "Source"},
    color_discrete_map={
        "Fossil Fuels": "#d62728",
        "Wind & Solar": "#1f77b4"
    }
)
st.plotly_chart(fig, use_container_width=True)

# Insights
with st.expander("📌 Key Insights"):
    st.markdown("""
    - **Fossil fuels still dominate**, contributing ~70% of global electricity generation as of 2023.
    - **Wind & Solar are rapidly growing** — their share has increased more than 120× since 2000.
    - **Tipping point**: Wind & Solar overtook hydro as a source of renewable electricity around 2020.
    """)

# Data Sources
with st.expander("📊 Data Sources Used"):
    st.markdown("""
    - `data/emberChartData.xlsx` – Coal generation (TWh)  
    - `data/emberChartData-_1_.xlsx` – Gas generation (TWh)  
    - `data/emberChartData-_2_.xlsx` – Wind & Solar generation (TWh)  
    """)
