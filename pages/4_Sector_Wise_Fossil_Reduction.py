import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(
    layout="wide",
    page_title="Global Oil Production Trends",
    page_icon="⛽"
)

@st.cache_data
def load_data():
    # 1) Read sheet, skipping the first metadata row
    df = pd.read_excel(
        "data/INT-Export-04-03-2025_21-40-52.xlsx",
        skiprows=1,       # skip the "Report generated on..." row
        header=0,         # use the next row as header
        dtype=str
    )
    # 2) Clean header names
    df.columns = df.columns.str.strip()
    # 3) Rename the first two columns into meaningful names
    df = df.rename(columns={df.columns[0]: "series_code", df.columns[1]: "series_name"})
    # 4) Detect year columns: any column whose header is exactly 4 digits
    year_cols = [col for col in df.columns if re.fullmatch(r"\d{4}", str(col))]
    # 5) Melt to long format
    df_long = df.melt(
        id_vars=["series_code", "series_name"],
        value_vars=year_cols,
        var_name="year",
        value_name="value"
    )
    # 6) Convert types
    df_long["year"] = df_long["year"].astype(int)
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
    # 7) Filter to the series you want
    keep = [
        "Total petroleum and other liquids (Mb/d)",
        "Crude oil, NGPL, and other liquids (Mb/d)",
        "Crude oil including lease condensate (Mb/d)"
    ]
    df_long = df_long[df_long["series_name"].isin(keep)]
    return df_long

df = load_data()

st.title("Global Petroleum Production by Series (1973–2023)")
st.markdown("""
Compare trends in:
- **Total petroleum and other liquids**  
- **Crude oil, NGPL, and other liquids**  
- **Crude oil including lease condensate**  
""")

fig = px.line(
    df,
    x="year",
    y="value",
    color="series_name",
    title="Global Oil & Liquids Production Over Time",
    labels={"value": "Mb/d", "year": "Year", "series_name": "Series"}
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📌 Narrative"):
    st.markdown("""
    - **Total petroleum and other liquids** is the broadest measure, including all liquids.  
    - **Crude oil, NGPL, and other liquids** tracks upstream production before processing.  
    - **Crude oil including lease condensate** isolates just the pure oil component.
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - `data/INT-Export-04-03-2025_21-40-52.xlsx`  
    - The first row was metadata (skipped), then header row with years 1973–2023.  
    """)
