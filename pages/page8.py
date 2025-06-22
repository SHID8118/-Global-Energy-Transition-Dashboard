# 4. Renewable Leaders (pages/4_🌿_Renewable_Leaders.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Renewable Leaders", page_icon="🌿")

@st.cache_data
def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    return df[df['year'] == 2023][['country', 'iso_code', 'renewables_share_elec']].dropna()

df = load_data()
leaders = df[df['renewables_share_elec'] > 50]

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌿 Countries with >50% Renewable Electricity (2023)")
with col2:
    st.download_button("Download Data", leaders.to_csv(index=False), "renewable_leaders.csv")

# Visualizations
fig1 = px.choropleth(
    leaders,
    locations="iso_code",
    color="renewables_share_elec",
    hover_name="country",
    title="Global Renewable Leaders Map"
)

fig2 = px.pie(
    leaders,
    names="country",
    values="renewables_share_elec",
    title="Renewable Share Distribution"
)

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)

# Country Details
with st.expander("Country Details"):
    st.markdown("""
    - **Iceland**: 100% (Hydro + Geothermal)
    - **Norway**: 98% (Hydro)
    - **Uruguay**: 95% (Wind)
    """)

with st.expander("Data Source"):
    st.markdown("OWID Energy Data (2023)")
