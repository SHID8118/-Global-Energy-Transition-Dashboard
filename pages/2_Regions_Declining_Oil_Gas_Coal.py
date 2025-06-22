import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Regions Declining Fossil Demand",
    page_icon="🌍"
)

@st.cache_data
def load_data():
    # Load the region-scenario table
    df = pd.read_excel("data/bpEO24-change-in-oil-demand-by-region.xlsx")
    # Rename the first column to 'scenario'
    df = df.rename(columns={"Year": "scenario"})
    
    # Melt so each row is one region–scenario pair
    long = df.melt(
        id_vars=["scenario"],
        value_vars=["Developed", "China", "Emerging ex. China", "Total"],
        var_name="region",
        value_name="demand_change_twh"
    )
    return long

df = load_data()

st.title("Which regions show consistent decline in oil/gas/coal demand?")
st.markdown("""
This chart compares projected changes in fossil demand (TWh) for key regions under two pathways:
- **Current Trajectory**  
- **Net Zero**  
""")

# Grouped bar chart
fig = px.bar(
    df,
    x="scenario",
    y="demand_change_twh",
    color="region",
    barmode="group",
    title="Projected Change in Fossil Demand by Region",
    labels={
        "scenario": "Pathway Scenario",
        "demand_change_twh": "Change in Demand (TWh)",
        "region": "Region"
    }
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📌 Narrative"):
    st.markdown("""
    - Under the **Net Zero** pathway, all regions cut demand far more sharply than under the current trajectory.  
    - “Developed” economies reduce by ~21 TWh vs ~8.6 TWh today, while “Emerging ex. China” drop by ~22 TWh vs +7 TWh under business-as-usual.  
    - China itself swings from a small increase under current policies to a ~9 TWh reduction in Net Zero.  
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - `data/bpEO24-change-in-oil-demand-by-region.xlsx`  
    - Table of projected fossil demand change (TWh) by region under two scenarios  
    """)
