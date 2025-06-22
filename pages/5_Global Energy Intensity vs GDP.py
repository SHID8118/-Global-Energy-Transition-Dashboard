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
This dashboard visualizes the change in global energy intensity — defined as the amount of energy used per unit of economic output — over time.
It helps track how efficiently the world is using energy as economies grow.
""")

@st.cache_data
@st.cache_data
def load_data():
    # Try skipping 0 to 5 rows (adjust as needed)
    df = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-World.xlsx", skiprows=3)
    
    df.columns = df.columns.str.strip()  # Clean column names

    # 👇 Debug print to show what columns were actually read
    st.write("Detected columns:", df.columns.tolist())

    if "Year" not in df.columns or "TES/GDP PPP" not in df.columns:
        st.error("Expected columns like 'Year' and 'TES/GDP PPP' not found.")
        return pd.DataFrame()

    df = df[["Year", "TES/GDP PPP"]].dropna()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype(int)
    df["TES/GDP PPP"] = pd.to_numeric(df["TES/GDP PPP"], errors="coerce")

    return df


df = load_data()

if df.empty:
    st.warning("No valid data available to display. Please check the Excel file format.")
else:
    # Plot
    fig = px.line(
        df,
        x="Year",
        y="TES/GDP PPP",
        markers=True,
        title="Global Energy Intensity (MJ per thousand 2015 USD PPP)",
        labels={
            "TES/GDP PPP": "MJ per 1000 USD (PPP)",
            "Year": "Year"
        },
    )
    fig.update_traces(line=dict(color="blue"))
    fig.update_layout(hovermode="x unified")

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📌 Narrative"):
        st.markdown("""
        - **Energy intensity** measures how much energy is used to produce economic output.
        - A **decline** in intensity suggests **greater energy efficiency** or a shift to less energy-intensive industries.
        - The values are expressed in **MJ per 1000 USD (2015 PPP)** — so lower is better.
        """)

    with st.expander("📊 Data Source"):
        st.markdown("""
        - Data Source: International Energy Agency or equivalent.
        - Excel column names should include:
            - `Year`
            - `TES/GDP PPP` (in MJ per 1000 USD PPP)
        """)
