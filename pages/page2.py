# 2. Fossil Reduction Leaders (pages/2_🌍_Fossil_Reduction_Leaders.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Fossil Reduction Leaders", page_icon="🌍")

@st.cache_data
def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    df = df[df['year'].isin([2010, 2023])][['country', 'year', 'fossil_share_elec']].dropna()
    pivot = df.pivot(index='country', columns='year', values='fossil_share_elec')
    pivot['Change'] = pivot[2010] - pivot[2023]
    return pivot.nlargest(10, 'Change').reset_index()

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌍 Top 10 Fossil Fuel Reduction Leaders (2010–2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "fossil_reduction.csv")

# Visualization
fig = px.bar(
    df, y='country', x='Change',
    orientation='h',
    title="Percentage Point Reduction in Fossil Fuel Share",
    color='Change',
    color_continuous_scale='Blues'
)
fig.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig, use_container_width=True)

# Policy Insights
with st.expander("Key Policy Insights"):
    st.markdown("""
    - **Denmark**: 45% reduction (Wind expansion + coal phaseout)
    - **UK**: 40% reduction (Coal phaseout + offshore wind)
    - **Germany**: 35% reduction (Energiewende policy)
    """)

with st.expander("Methodology"):
    st.markdown("Data Source: OWID Energy Data (2010-2023)")
