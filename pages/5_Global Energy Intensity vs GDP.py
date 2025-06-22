import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Energy Intensity",
    layout="wide",
    page_icon="📉"
)

st.title("📉 Global Energy Intensity Over Time")

st.markdown("""
This dashboard visualizes the **change in global energy intensity** — defined as the amount of energy used per unit of economic output — over time.
It helps track how efficiently the world is using energy as economies grow.
""")

@st.cache_data
def load_data():
    # Skip metadata rows; actual data starts from row 4 (index 3)
    df = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-World.xlsx", skiprows=3)
    
    # Strip any extra spaces from column headers
    df.columns = df.columns.str.strip()
    
    # Try to find the correct column automatically
    energy_col = None
    for col in df.columns:
        if "TES" in col and "GJ" in col and "GDP" in col:
            energy_col = col
            break

    if energy_col is None or "Year" not in df.columns:
        st.error("Expected columns like 'Year' and 'TES (GJ per USD GDP PPP)' not found.")
        return pd.DataFrame()

    df = df[["Year", energy_col]].dropna()
    df = df.rename(columns={energy_col: "Energy Intensity (GJ per USD GDP PPP)"})
    
    # Convert types
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype(int)
    df["Energy Intensity (GJ per USD GDP PPP)"] = pd.to_numeric(df["Energy Intensity (GJ per USD GDP PPP)"], errors="coerce")

    return df

df = load_data()

if df.empty:
    st.warning("No valid data available to display. Please check the Excel file format.")
else:
    # Plot
    fig = px.line(
        df,
        x="Year",
        y="Energy Intensity (GJ per USD GDP PPP)",
        markers=True,
        title="Global Energy Intensity (GJ per USD GDP PPP)",
        labels={"Energy Intensity (GJ per USD GDP PPP)": "GJ per USD (PPP)", "Year": "Year"},
    )
    fig.update_traces(line=dict(color="green"))
    fig.update_layout(hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📌 Narrative"):
        st.markdown("""
        - **Energy intensity** is a key indicator of energy efficiency.
        - A **declining trend** implies the world is using **less energy per unit of GDP**, which is generally a positive sign.
        - It can reflect improvements in technology, structural economic shifts, or changes in energy consumption behavior.
        """)

    with st.expander("📊 Data Source"):
        st.markdown("""
        - The data is sourced from the **International Energy Agency (IEA)** or equivalent reliable sources.
        - The original Excel file should have the actual data starting from **row 4**, with columns like:
            - `Year`
            - `TES (GJ per USD GDP PPP)`
        """)
