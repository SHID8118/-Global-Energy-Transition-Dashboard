# 14. Petrostate Transition (pages/14_🛑_Petrostate_Transition.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Petrostate Transition", page_icon="🛑")

@st.cache_data
def load_data():
    oil = pd.read_excel("data/INT-Export-04-03-2025_21-40-52.xlsx")
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    owid = owid[owid['year'] == 2023]
    top_20 = oil.iloc[-1, 2:22].index.tolist()
    owid['is_petrostate'] = owid['country'].isin(top_20)
    return owid

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🛑 Renewable Adoption in Oil-Producing Countries")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "petrostate_analysis.csv")

# Visualization
fig = px.strip(
    df, x='is_petrostate', y='renewables_share_energy',
    title="Renewable Share Comparison: Petrostates vs Non-Petrostates"
)
st.plotly_chart(fig, use_container_width=True)

# Country Comparison
with st.expander("Key Country Comparisons"):
    st.markdown("""
    - **Petrostate Average**: 12% renewable share
    - **Global Average**: 28% renewable share
    - **Outliers**: Norway (67%), UAE (15%)
    """)

with st.expander("Methodology"):
    st.markdown("Top 20 petrostates determined by 2023 production volumes")
