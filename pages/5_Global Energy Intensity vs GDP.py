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
def load_data():
    df = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-World.xlsx", skiprows=3)
    df.columns = df.columns.str.strip()

    if "Year" not in df.columns or "TES/GDP" not in df.columns:
        st.error("Expected columns like 'Year' and 'TES/GDP' not found.")
        return pd.DataFrame()

    df = df[["Year", "TES/GDP"]].dropna()
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype(int)
    df["TES/GDP"] = pd.to_numeric(df["TES/GDP"], errors="coerce")

    return df


df = load_data()

if df.empty:
    st.warning("No valid data available to display. Please check the Excel file format.")
else:
    # Plot
    import plotly.express as px

fig = px.line(
    df,
    x="Year",
    y="TES/GDP",
    title="📉 Global Energy Intensity Over Time",
    labels={
        "Year": "Year",
        "TES/GDP": "Energy Intensity (MJ/thousand 2015 USD)"
    }
)
st.plotly_chart(fig, use_container_width=True)

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
