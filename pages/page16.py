# 16. COVID Impact (pages/16_🦠_COVID_Energy_Impact.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="COVID Energy Impact", page_icon="🦠")

@st.cache_data
def load_data():
    tes = pd.read_excel("data/Total-energy-supply-_TES_-by-source-World.xlsx")
    tes['Total'] = tes.sum(axis=1)
    return tes.pct_change().loc[2019:2021]

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🦠 COVID-19 Impact on Energy Demand (2019–2021)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "covid_impact.csv")

# Visualization
fig = px.waterfall(
    df, x=df.index, y='Total',
    title="Year-over-Year Change in Energy Demand"
)
st.plotly_chart(fig, use_container_width=True)

# Sector Analysis
with st.expander("Sectoral Impact"):
    st.markdown("""
    - **2020 Total Decline**: -5% overall demand
    - **Oil**: -9% (transportation impact)
    - **Electricity**: -2% (industrial slowdown)
    """)

with st.expander("Methodology"):
    st.markdown("Data from Total Energy Supply by Source dataset")
