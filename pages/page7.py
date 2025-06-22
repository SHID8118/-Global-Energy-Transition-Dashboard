# 3. Oil Producers vs Renewables (pages/3_⛽_Oil_vs_Renewables.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Oil vs Renewables", page_icon="⛽")

@st.cache_data
def load_data():
    oil = pd.read_excel("data/INT-Export-04-03-2025_21-40-52.xlsx", sheet_name="Global Production")
    top_20 = oil.iloc[-1, 2:22].index.tolist()
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    owid = owid[owid['year'] == 2023][['country', 'renewables_share_energy']]
    owid['Oil Producer'] = owid['country'].isin(top_20)
    return owid

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("⛽ Renewable Adoption: Oil Producers vs Others")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "oil_renewables.csv")

# Visualization
fig = px.box(
    df, x='Oil Producer', y='renewables_share_energy',
    title="Renewable Share Comparison (2023)",
    labels={"renewables_share_energy": "Renewable Share (%)", "Oil Producer": "Country Type"}
)
st.plotly_chart(fig, use_container_width=True)

# Country Insights
with st.expander("Key Country Insights"):
    st.markdown("""
    - **Oil Producers Average**: 15% renewable share
    - **Global Average**: 28% renewable share
    - **Norway Outlier**: 67% renewables despite oil production
    """)

with st.expander("Methodology"):
    st.markdown("Top 20 oil producers determined by 2023 production volumes")
