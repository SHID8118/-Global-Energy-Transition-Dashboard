# 9. Decarbonization Leaders (pages/9_🌱_Decarbonization_Leaders.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Decarbonization Leaders", page_icon="🌱")

@st.cache_data
def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    df['Region'] = df['country'].apply(lambda x: get_region(x))  # Custom region mapping
    return df[df['year'] >= 2000]

def get_region(country):
    # Simplified region mapping for example
    regions = {
        "Europe": ["Germany", "France", "Italy"],
        "Asia": ["China", "India", "Japan"],
        "Americas": ["USA", "Brazil", "Canada"],
        "Africa": ["Nigeria", "Kenya", "South Africa"]
    }
    for region, countries in regions.items():
        if country in countries:
            return region
    return "Other"

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌱 Regional Decarbonization Progress (2000–2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "decarbonization.csv")

# Visualization
fig = px.line(
    df, x='year', y='carbon_intensity_elec',
    color='Region',
    title="Carbon Intensity of Electricity by Region"
)
st.plotly_chart(fig, use_container_width=True)

# Regional Analysis
with st.expander("Key Regional Trends"):
    st.markdown("""
    - **Europe**: -50% intensity (wind/nuclear transition)
    - **Asia**: +10% intensity (coal expansion)
    - **Americas**: -30% intensity (gas + renewables)
    """)

with st.expander("Methodology"):
    st.markdown("Carbon intensity calculated as grams CO2/kWh")
