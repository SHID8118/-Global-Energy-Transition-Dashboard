# pages/5_Countries_Growing_Renewables.py

import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Global Growth in Renewable Energy Share",
    layout="wide",
    page_icon="🌍"
)

st.title("🌍 Global Growth in Renewable Energy Share")
st.markdown("""
This dashboard explores the global progress in the share of **modern renewables** in final energy consumption, as defined under **SDG 7.2**.
It reflects how the world's energy consumption is becoming cleaner over time.
""")

@st.cache_data
def load_data():
    df = pd.read_excel("data/Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx", skiprows=0)
    df.columns = df.columns.str.strip()
    df = df.rename(columns={
        "Year": "Year",
        "Share of modern renewables": "Renewable Share (%)"
    })
    df = df[["Year", "Renewable Share (%)"]]
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    df["Renewable Share (%)"] = pd.to_numeric(df["Renewable Share (%)"], errors="coerce")
    return df.dropna()

# Load data
df = load_data()

# Preview
st.subheader("Data Preview")
st.dataframe(df.head())

# Line Chart
fig = px.line(
    df,
    x="Year",
    y="Renewable Share (%)",
    title="Global Renewable Energy Share in Final Energy Consumption (SDG 7.2)",
    markers=True,
    labels={"Renewable Share (%)": "% of Final Energy Consumption"}
)
fig.update_traces(line_color="green")
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Key Insights
with st.expander("📌 Key Insights"):
    st.markdown("""
    - The data shows how the **global share of modern renewable energy** has evolved over time.
    - **Consistent growth** indicates global investment and transition to sustainable energy sources.
    - This metric helps assess the world’s progress toward **Sustainable Development Goal 7.2**.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - **File:** `Renewable-share-_modern-renewables_-in-final-energy-consumption-_SDG-7.2_-World.xlsx`
    - **Entity:** Global (World-level data only)
    - **Columns Used:** `Year`, `Share of modern renewables`
    - **Source:** IEA Sustainable Development Goal 7: [IEA SDG 7 Report](https://www.iea.org/reports/tracking-sdg7-the-energy-progress-report-2022)
    """)
