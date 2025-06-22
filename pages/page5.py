# 1. Fossil vs Renewables (pages/1_📉_Fossil_vs_Renewables.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Fossil vs Renewables", page_icon="📉")

@st.cache_data
def load_data():
    coal = pd.read_excel("data/emberChartData.xlsx")
    gas = pd.read_excel("data/emberChartData-_1_.xlsx")
    wind_solar = pd.read_excel("data/emberChartData-_2_.xlsx")
    df = pd.merge(coal, gas, on="Year").merge(wind_solar, on="Year")
    df["Fossil Fuels"] = df["Coal"] + df["Gas"]
    return df

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📉 Global Fossil vs Renewable Energy Trends (2000–2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "fossil_renewables.csv")

# Visualization
fig = px.area(
    df, x="Year", y=["Fossil Fuels", "Wind & Solar"],
    title="Global Electricity Generation Mix",
    labels={"value": "TWh", "variable": "Source"}
)
st.plotly_chart(fig, use_container_width=True)

# Insights
with st.expander("Key Insights"):
    st.markdown("""
    - **Fossil fuels dominate**: 70% of electricity generation in 2023
    - **Renewables growth**: 120x increase since 2000
    - **Tipping point**: Wind/solar surpassed hydro in 2020
    """)

with st.expander("Data Sources"):
    st.markdown("""
    - Coal/Gas: Ember Global Electricity Review  
    - Wind/Solar: Ember Renewable Energy Dataset
    """)
