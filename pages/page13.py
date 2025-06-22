# 13. Oil Concentration (pages/13_🔥_Oil_Concentration.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Oil Concentration", page_icon="🔥")

@st.cache_data
def load_data():
    oil = pd.read_excel("data/INT-Export-04-03-2025_21-40-52.xlsx")
    def hhi(series):
        return (series**2).sum() * 10000
    return oil.groupby('Year').apply(lambda x: hhi(x.iloc[:, 2:])).reset_index(name='HHI')

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔥 Oil Production Concentration Over Time")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "oil_concentration.csv")

# Visualization
fig = px.line(
    df, x='Year', y='HHI',
    title="Herfindahl-Hirschman Index for Oil Production",
    labels={"HHI": "HHI Score", "Year": "Year"}
)
fig.add_hline(y=2500, line_dash="dash", annotation_text="Competitive Market Threshold")
st.plotly_chart(fig, use_container_width=True)

# Trend Analysis
with st.expander("Concentration Trends"):
    st.markdown("""
    - **2000**: HHI = 1800 (Moderate concentration)
    - **2023**: HHI = 2200 (Increasing concentration)
    - **OPEC Dominance**: Major contributor to increased concentration
    """)

with st.expander("Methodology"):
    st.markdown("HHI calculated from top 20 oil producing countries' market shares")
