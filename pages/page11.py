# 7. Energy Industrialization (pages/7_⚙️_Energy_Industrialization.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Energy Industrialization", page_icon="⚙️")

@st.cache_data
def load_data():
    tes = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-World.xlsx")
    wb = pd.read_csv("data/wb_manufacturing_gdp.csv")
    return pd.merge(tes, wb, on=['country', 'year'])

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("⚙️ Energy Intensity vs Industrialization (2022)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "energy_industrialization.csv")

# Visualization
fig = px.scatter(
    df[df['year'] == 2022],
    x='TES_per_GDP', y='manufacturing_pct',
    size='population',
    hover_name='country',
    title="Energy Intensity vs Manufacturing Contribution to GDP"
)
st.plotly_chart(fig, use_container_width=True)

# Case Studies
with st.expander("Key Observations"):
    st.markdown("""
    - **China**: High intensity (heavy industry) with 40% manufacturing share
    - **Germany**: Moderate intensity with 25% manufacturing share
    - **USA**: Low intensity with 15% manufacturing share
    """)

with st.expander("Data Sources"):
    st.markdown("TES/GDP from IEA, Manufacturing data from World Bank")
