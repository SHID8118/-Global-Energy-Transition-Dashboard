import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Fossil vs Renewables", page_icon="📉")
df = pd.read_excel("data/emberChartData.xlsx")
st.write("Unique variable names:", df["variable"].unique())
st.stop()  # halt execution so you can see the output

@st.cache_data
def load_data():
    df = pd.read_excel("data/emberChartData.xlsx")
    df.columns = df.columns.str.strip().str.lower()

    # Filter only required variables
    df = df[df['variable'].isin(['coal', 'gas', 'wind and solar'])]
    
    # Pivot to wide format
    df_pivot = df.pivot_table(index="year", columns="variable", values="generation_twh", aggfunc="sum").reset_index()

    # Rename for clarity
    df_pivot.rename(columns={
        "coal": "Coal",
        "gas": "Gas",
        "wind and solar": "Wind & Solar"
    }, inplace=True)

    # Add derived column
    df_pivot["Fossil Fuels"] = df_pivot["Coal"] + df_pivot["Gas"]
    return df_pivot

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("📉 Global Fossil vs Renewable Energy Trends (2000–2023)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "fossil_vs_renewables.csv")

# Visualization
fig = px.area(
    df,
    x="year",
    y=["Fossil Fuels", "Wind & Solar"],
    title="Global Electricity Generation Mix",
    labels={"value": "TWh", "variable": "Source"},
    color_discrete_map={
        "Fossil Fuels": "#d62728",
        "Wind & Solar": "#1f77b4"
    }
)
st.plotly_chart(fig, use_container_width=True)

# Narrative / Insights
with st.expander("📌 Key Insights"):
    st.markdown("""
    - **Fossil fuels still dominate**, contributing ~70% of global electricity generation as of 2023.
    - **Wind & Solar are rapidly growing** — their share has increased more than 120× since 2000.
    - **Tipping point**: Wind & solar overtook hydro as a source of renewable electricity around 2020.
    """)

with st.expander("📊 Data Sources Used"):
    st.markdown("""
    - `emberChartData.xlsx`  
    - Source: [Ember Climate Global Electricity Review](https://ember-climate.org/)  
    - Filtered for: **Coal, Gas, Wind and Solar** generation (TWh)  
    """)
