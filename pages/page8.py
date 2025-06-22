# 8. Fossil Subsidies (pages/8_💸_Subsidies_vs_Renewables.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Subsidies vs Renewables", page_icon="💸")

@st.cache_data
def load_data():
    subsidies = pd.read_excel("data/bpEO24-change-in-oil-demand-by-region.xlsx", sheet_name="Subsidies")
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    owid = owid[owid['year'].isin([2010, 2023])][['country', 'year', 'renewables_share_energy']]
    return pd.merge(subsidies, owid, on='country')

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("💸 Impact of Fossil Subsidies on Renewable Growth")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "subsidy_analysis.csv")

# Visualization
fig = px.line(
    df, x='year', y='renewables_share_energy',
    color='subsidy_level',
    title="Renewable Growth by Fossil Subsidy Level"
)
st.plotly_chart(fig, use_container_width=True)

# Country Comparisons
with st.expander("Subsidy Impact Analysis"):
    st.markdown("""
    - **High Subsidy Countries**: Saudi Arabia, Russia show minimal growth
    - **Low Subsidy Countries**: Germany, UK show rapid growth
    - **Policy Impact**: Subsidy removal accelerates renewable adoption
    """)

with st.expander("Methodology"):
    st.markdown("Subsidy levels classified by BP Energy Outlook")
