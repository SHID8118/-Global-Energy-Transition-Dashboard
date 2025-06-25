# pages/8_Renewables_vs_Fossil_Reduction.py

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Renewables vs Fossil Reduction",
    layout="wide",
    page_icon="♻️"
)

st.title("♻️ Renewables Growth vs Fossil Reduction")
st.markdown("""
This dashboard visualizes the relationship between **renewable energy share** and **fossil fuel consumption** across countries
based on the latest available data.
""")

@st.cache_data
def load_data():
    df = pd.read_excel("data/owid-energy-data.xlsx")

    # Ensure column names are stripped and lowercased for consistency
    df.columns = df.columns.str.strip()

    # Expected columns
    cols_needed = [
        "country", "Year",
        "coal_consumption", "oil_consumption", "gas_consumption",
        "renewables_share_energy"
    ]

    # Ensure all expected columns exist in the DataFrame
    missing_cols = [col for col in cols_needed if col not in df.columns]
    if missing_cols:
        st.error(f"The following required columns are missing from the dataset: {missing_cols}")
        st.stop()

    # Filter for latest year available in the dataset
    latest_year = df["year"].max()
    df_latest = df[df["year"] == latest_year][cols_needed]

    # Drop rows with missing values
    df_latest.dropna(inplace=True)

    # Calculate total fossil fuel consumption
    df_latest["fossil_consumption"] = df_latest[[
        "coal_consumption", "oil_consumption", "gas_consumption"
    ]].sum(axis=1)

    return df_latest, latest_year

# Load and prepare data
df, latest_year = load_data()

# Plot
fig = px.scatter(
    df,
    x="renewables_share_energy",
    y="fossil_consumption",
    hover_name="country",
    title=f"Renewables Share vs Fossil Fuel Consumption ({latest_year})",
    labels={
        "renewables_share_energy": "Renewables Share in Energy (%)",
        "fossil_consumption": "Total Fossil Fuel Consumption (TWh)"
    },
    color="renewables_share_energy",
    size="fossil_consumption",
    height=600
)
fig.update_layout(hovermode="closest")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Key Insights"):
    st.markdown(f"""
    - The scatter plot shows how countries vary in **renewables share** vs **fossil consumption**.
    - Countries in the top-left tend to be **low fossil users** with **high renewable share**, showing clean energy leadership.
    - Countries in the bottom-right rely heavily on fossil fuels and lag in renewables.
    - This helps assess correlation between **clean energy adoption** and **reduction in fossil reliance**.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **File:** `owid-energy-data.xlsx`
    - **Columns Used:** `country`, `year`, `coal_consumption`, `oil_consumption`, `gas_consumption`, `renewables_share_energy`
    - **Filtered for Latest Year**: {latest_year}
    """)
