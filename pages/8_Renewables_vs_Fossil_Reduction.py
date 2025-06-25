import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Renewables vs Fossil Correlation", page_icon="🔗")

@st.cache_data
def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    if 'year' not in df.columns:
        raise KeyError("The 'year' column is missing.")
    latest_year = df['year'].max()
    df_latest = df[df['year'] == latest_year]
    df_latest = df_latest[['country', 'renewables_share_energy', 'fossil_fuel_consumption']]
    df_latest = df_latest.dropna(subset=['country', 'renewables_share_energy', 'fossil_fuel_consumption'])
    return df_latest, latest_year

# Load data
df, year = load_data()

# Title and description
st.title("Renewables Growth vs Fossil Reduction Correlation")
st.markdown(f"""
This scatter plot compares countries' **renewable energy share** and **fossil fuel consumption** in the year **{year}**.
""")

# Country selection
default_countries = df['country'].unique().tolist()
selected_countries = st.multiselect("Select countries to display:", default_countries, default=default_countries)

# Filter based on selection
filtered_df = df[df['country'].isin(selected_countries)]

# Plot
fig = px.scatter(
    filtered_df,
    x="renewables_share_energy",
    y="fossil_fuel_consumption",
    hover_name="country",
    title=f"Renewable Share vs Fossil Fuel Consumption ({year})",
    labels={
        "renewables_share_energy": "Renewable Share (%)",
        "fossil_fuel_consumption": "Fossil Consumption (TWh)"
    }
)
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Narrative"):
    st.markdown("""
    Generally, countries with **higher renewable share** tend to have **lower fossil consumption**, but many exceptions exist based on energy needs and policies.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - Source: [OWID Energy Data](https://github.com/owid/energy-data)
    - File used: `owid-energy-data.xlsx`
    """)
