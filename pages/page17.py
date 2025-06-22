# 17. Energy Justice (pages/17_🏜️_Energy_Justice.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Energy Justice", page_icon="🏜️")

@st.cache_data
def load_data():
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    wb = pd.read_csv("data/wb_income.csv")
    df = pd.merge(owid, wb, on='country')
    return df[(df['income_group'] == 'Low income') & (df['renewables_share_energy'] > 30)]

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🏜️ Renewable Potential vs Investment in Low-Income Countries")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "energy_justice.csv")

# Visualization
fig = px.scatter(
    df, x='renewables_potential', y='renewables_share_energy',
    color='income_group',
    hover_name='country',
    title="Renewable Potential vs Actual Investment"
)
st.plotly_chart(fig, use_container_width=True)

# Country Examples
with st.expander("Underserved Countries"):
    st.markdown("""
    - **Niger**: High solar potential but <5% adoption
    - **Sudan**: Abundant solar resources with limited development
    - **Ethiopia**: Hydro potential underutilized
    """)

with st.expander("Methodology"):
    st.markdown("Income groups from World Bank data, potential from IEA assessments")
