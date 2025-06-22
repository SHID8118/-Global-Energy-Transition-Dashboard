# 5. GDP vs Renewables (pages/5_💰_Wealth_vs_Renewables.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Wealth vs Renewables", page_icon="💰")

@st.cache_data
def load_data():
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    wind_solar = pd.read_excel("data/emberChartData-_2_.xlsx")
    df = owid[owid['year'] == 2023]
    df['GDP Quintile'] = pd.qcut(df['gdp'], q=5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
    return pd.merge(df, wind_solar, left_on='country', right_on='Country')

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("💰 Wind vs Solar Adoption by GDP Quintile (2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "gdp_renewables.csv")

# Visualization
fig = px.bar(
    df.groupby('GDP Quintile')[['Wind', 'Solar']].mean().reset_index(),
    x='GDP Quintile', 
    y=['Wind', 'Solar'],
    barmode='group',
    title="Average Wind vs Solar Generation by Wealth Quintile"
)
st.plotly_chart(fig, use_container_width=True)

# Insights
with st.expander("Key Insights"):
    st.markdown("""
    - **Q5 (Richest)**: Lead in solar adoption (rooftop subsidies)
    - **Q3 (Middle)**: Highest wind adoption (onshore farms)
    - **Q1 (Poorest)**: Minimal renewable generation
    """)

with st.expander("Methodology"):
    st.markdown("GDP data from OWID, Wind/Solar data from Ember")
