# 15. Renewable Tipping Points (pages/15_📊_Renewable_Tipping_Points.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Renewable Tipping Points", page_icon="📊")

@st.cache_data
def load_data():
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    countries = ['Germany', 'UK', 'Denmark']
    df = owid[owid['country'].isin(countries)]
    df['Fossil'] = df['fossil_share_energy']
    df['Renewable'] = df['renewables_share_energy']
    return df

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📊 Renewable Tipping Points: Fossil vs Renewables Timeline")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "tipping_points.csv")

# Visualization
fig = px.line(
    df, x='year', y=['Fossil', 'Renewable'],
    color='country',
    title="Fossil vs Renewable Generation Over Time"
)
st.plotly_chart(fig, use_container_width=True)

# Historical Analysis
with st.expander("Key Historical Milestones"):
    st.markdown("""
    - **Denmark**: Renewables > Fossils (2015)
    - **Germany**: Renewables > Fossils (2022)
    - **UK**: Renewables > Fossils (2019)
    """)

with st.expander("Methodology"):
    st.markdown("Data from OWID Energy Database (2000-2023)")
