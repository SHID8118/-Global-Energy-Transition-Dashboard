import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Regions Declining Fossil Demand", page_icon="🌍")

@st.cache_data
def load_data():
    # assume this file has columns: region, year, oil_demand_twh, gas_demand_twh, coal_demand_twh
    df = pd.read_excel("data/bpEO24-change-in-oil-demand-by-region.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={
        "oil_demand_twh": "Oil",
        "gas_demand_twh": "Gas",
        "coal_demand_twh": "Coal"
    })
    # pick top 5 regions with largest decline from 2010 to latest
    df_period = df[df["year"].isin([2010, df["year"].max()])]
    pivot = df_period.pivot(index="region", columns="year", values=["Oil", "Gas", "Coal"])
    declines = ((pivot.xs(df["year"].max(), axis=1, level=1) - pivot.xs(2010, axis=1, level=1))
                .sum(axis=1)).sort_values()
    top5 = declines.head(5).index.tolist()
    return df[df["region"].isin(top5)]

df = load_data()

st.title("Which regions show consistent decline in oil/gas/coal demand?")
st.markdown("""
We look at the 5 regions with the largest absolute decline in fossil energy demand between 2010 and today.
""")

fig = px.line(
    df, x="year", y=["Oil", "Gas", "Coal"], color="region",
    title="Fossil Demand Trend for Top 5 Declining Regions",
    labels={"value": "TWh", "variable": "Fuel"}
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📌 Narrative"):
    st.markdown("""
    These regions have reduced fossil demand most sharply, driven by declining industrial output,
    fuel switching and efficiency measures.
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - `data/bpEO24-change-in-oil-demand-by-region.xlsx`  
    - Columns: `region`, `year`, `oil_demand_twh`, `gas_demand_twh`, `coal_demand_twh`
    """)
