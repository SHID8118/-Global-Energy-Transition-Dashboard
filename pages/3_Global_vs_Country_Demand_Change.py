import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Global vs Country Demand",
    page_icon="🌐"
)

@st.cache_data
def load_data():
    # Load OWID energy data
    df = pd.read_excel("data/owid-energy-data.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    
    # Calculate total fossil consumption per country-year
    df['fossil_total'] = (
        df.get('coal_consumption', 0).fillna(0) +
        df.get('oil_consumption', 0).fillna(0) +
        df.get('gas_consumption', 0).fillna(0)
    )
    
    # Filter for years >= 2000
    df = df[df['year'] >= 2000]
    
    # Global aggregate
    global_df = df.groupby('year', as_index=False)['fossil_total'] \
                  .sum() \
                  .assign(country='Global')
    
    # Specific countries
    countries = ['United States', 'China', 'India']
    country_df = df[df['country'].isin(countries)][['year', 'country', 'fossil_total']]
    
    # Combine
    return pd.concat([global_df, country_df], ignore_index=True)

df = load_data()

st.title("Global vs Specific Countries Fossil Demand")
st.markdown("""
Compare total fossil energy demand for the world versus the United States, China, and India since 2000.
""")

fig = px.line(
    df,
    x='year',
    y='fossil_total',
    color='country',
    title='Fossil Fuel Consumption over Time (2000–2023)',
    labels={
        'year': 'Year',
        'fossil_total': 'Total Fossil Consumption (TWh)',
        'country': 'Entity'
    }
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📌 Narrative"):
    st.markdown("""
    - **Global trend** rises steadily, reflecting overall energy demand growth.  
    - **China** has the steepest increase through the 2010s, peaking around 2020.  
    - **United States** shows a plateau and gradual decline post-2008 financial crisis.  
    - **India** continues to climb, driven by industrialization and population growth.
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - `data/owid-energy-data.xlsx`  
    - Columns used: `country`, `year`, `coal_consumption`, `oil_consumption`, `gas_consumption`
    """)
