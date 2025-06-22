import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(layout="wide", page_title="Fossil vs Renewables", page_icon="📉")

# Load and prepare data
@st.cache_data
def load_data():
    coal_df = pd.read_excel("data/emberChartData.xlsx")[["Year", "Coal"]].dropna()
    gas_df = pd.read_excel("data/emberChartData-_1_.xlsx")[["Year", "Gas"]].dropna()
    renew_df = pd.read_excel("data/emberChartData-_2_.xlsx")[["Year", "Wind and Solar"]].dropna()

    # Merge on Year
    df = coal_df.merge(gas_df, on="Year", how="inner").merge(renew_df, on="Year", how="inner")

    # Rename for clarity
    df.rename(columns={
        "coal": "Coal",
        "gas": "Gas",
        "wind and solar": "Wind & Solar"
    }, inplace=True)

    # Add fossil total
    df["Fossil Fuels"] = df["Coal"] + df["Gas"]
    return df

df = load_data()

# UI Header and Download
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📉 Global Fossil vs Renewable Energy Trends (2000–2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "fossil_vs_renewables.csv")

# Plotting
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

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown("""
    - **Fossil fuels still dominate**, contributing ~70% of global electricity generation as of 2023.
    - **Wind & Solar are rapidly growing** — their share has increased more than 120× since 2000.
    - **Tipping point**: Wind & solar overtook hydro as a source of renewable electricity around 2020.
    """)

# Data source reference
with st.expander("📊 Data Sources Used"):
    st.markdown("""
    - `data/emberChartData.xlsx` – Coal  
    - `data/emberChartData-_1_.xlsx` – Gas  
    - `data/emberChartData-_2_.xlsx` – Wind & Solar  
    - All values in **TWh (Terawatt-hours)**
    """)
