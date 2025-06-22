import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Global Oil Production Trends",
    page_icon="⛽"
)

@st.cache_data
def load_data():
    # 1. Read the sheet, skipping the first two rows of metadata
    df = pd.read_excel(
        "data/INT-Export-04-03-2025_21-40-52.xlsx",
        skiprows=2,
        dtype=str
    )
    # 2. Clean column names
    df.columns = df.columns.str.strip()
    
    # 3. Melt years into long format
    year_cols = [col for col in df.columns if col.isdigit()]
    df_long = df.melt(
        id_vars=["INTL.53-1-WORL-TBPD.A", "Total petroleum and other liquids (Mb/d)"],
        value_vars=year_cols,
        var_name="year",
        value_name="value"
    )
    # 4. Rename the series columns
    df_long = df_long.rename(columns={
        "INTL.53-1-WORL-TBPD.A": "series_code",
        "Total petroleum and other liquids (Mb/d)": "series_name"
    })
    # 5. Filter to the three main series you want
    keep = [
        "Total petroleum and other liquids (Mb/d)",
        "Crude oil, NGPL, and other liquids (Mb/d)",
        "Crude oil including lease condensate (Mb/d)"
    ]
    df_long = df_long[df_long["series_name"].isin(keep)]
    # 6. Convert year & value to numeric
    df_long["year"] = df_long["year"].astype(int)
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
    return df_long

df = load_data()

st.title("Global Petroleum Production by Series (1973–2023)")
st.markdown("""
Compare trends in:
- **Total liquids**  
- **Crude oil & NGPL**  
- **Crude oil (condensate)**  
""")

fig = px.line(
    df,
    x="year",
    y="value",
    color="series_name",
    title="Global Oil & Liquids Production Over Time",
    labels={"value":"Mb/d","year":"Year","series_name":"Series"}
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📌 Narrative"):
    st.markdown("""
    - **Total liquids** includes everything—this is the broadest measure.  
    - **Crude oil & NGPL** tracks upstream liquids before processing.  
    - **Crude oil (condensate)** isolates just the oil component.
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - `data/INT-Export-04-03-2025_21-40-52.xlsx`  
    - Rows: each production series; Columns: years 1973–2023  
    """)
