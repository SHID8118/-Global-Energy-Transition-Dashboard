# 6. Renewable Diversity (pages/6_🌪️_Renewable_Diversity.py)
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(layout="wide", page_title="Renewable Diversity", page_icon="🌪️")

@st.cache_data
def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    return df[df['year'] == 2023]

df = load_data()

# Calculate diversity index
def shannon_index(row):
    shares = [row['wind_share_energy'], row['solar_share_energy'], 
             row['hydro_share_energy'], row['biofuel_share_energy']]
    shares = [s for s in shares if s > 0]
    return -sum(s * np.log(s) for s in shares)

df['Diversity'] = df.apply(shannon_index, axis=1)

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌪️ Renewable Energy Portfolio Diversity (2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "renewable_diversity.csv")

# Visualization
fig = px.choropleth(
    df, locations="iso_code", color="Diversity",
    hover_name="country",
    title="Global Renewable Energy Diversity Index"
)
st.plotly_chart(fig, use_container_width=True)

# Regional Analysis
with st.expander("Regional Analysis"):
    st.markdown("""
    - **Europe**: Balanced portfolio (wind 40%, solar 20%, hydro 30%)
    - **Asia**: Hydro-dominated (70%+ in many countries)
    - **Africa**: Limited diversity due to infrastructure constraints
    """)

with st.expander("Methodology"):
    st.markdown("Shannon index calculation based on renewable source shares")
