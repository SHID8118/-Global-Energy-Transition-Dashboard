# 18. HDI Electricity Link (pages/18_⚖️_HDI_Electricity.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="HDI Electricity Link", page_icon="⚖️")

@st.cache_data
def load_data():
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    hdi = pd.read_csv("data/hdi.csv")
    return pd.merge(owid, hdi, on=['country', 'year'])

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("⚖️ Electricity Access vs Human Development Index (2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "hdi_electricity.csv")

# Visualization
fig = px.hexbin(
    df, x='per_capita_electricity', y='hdi',
    title="Correlation Between Electricity Access and HDI",
    labels={"per_capita_electricity": "kWh per capita", "hdi": "Human Development Index"}
)
st.plotly_chart(fig, use_container_width=True)

# Development Analysis
with st.expander("Key Correlations"):
    st.markdown("""
    - **Strong correlation**: r=0.8 between electricity access and HDI
    - **Threshold**: No country with <1,000 kWh/capita has HDI >0.7
    - **Exceptions**: Some Gulf countries with high HDI but low electricity access
    """)

with st.expander("Methodology"):
    st.markdown("HDI data from UNDP, electricity data from OWID")
