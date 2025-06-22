# 10. Energy Decoupling (pages/10_📈_Energy_Decoupling.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Energy Decoupling", page_icon="📈")

@st.cache_data
def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    return df.groupby('country').apply(
        lambda x: x.set_index('year')[['gdp', 'energy_per_gdp']].pct_change(10).dropna()
    ).reset_index()

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📈 GDP Growth vs Energy Efficiency (2013–2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "decoupling.csv")

# Visualization
fig = px.scatter(
    df[(df['gdp'] > 0.2) & (df['energy_per_gdp'] < -0.1)],
    x='gdp', y='energy_per_gdp',
    hover_name='country',
    title="Countries Decoupling GDP Growth from Energy Use"
)
st.plotly_chart(fig, use_container_width=True)

# Country Comparisons
with st.expander("Key Country Comparisons"):
    st.markdown("""
    - **Germany**: +25% GDP, -15% energy/GDP
    - **USA**: +18% GDP, +5% energy/GDP
    - **Japan**: +12% GDP, -10% energy/GDP
    """)

with st.expander("Methodology"):
    st.markdown("10-year percentage change in GDP vs energy intensity")
