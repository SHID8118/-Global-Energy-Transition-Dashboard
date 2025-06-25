import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(
    layout="wide",
    page_title="Production by Country",
    page_icon="🌐"
)

st.title("🌐 Petroleum & Liquids Production by Country")
st.markdown("""
Select a country (or “World”) to see how its various petroleum‐liquid production series 
evolved from 1973–2023.
""")

@st.cache_data
def load_data():
    # 1) Read the sheet, skipping the first metadata row
    df = pd.read_excel(
        "data/INT-Export-04-03-2025_21-40-52.xlsx",
        skiprows=1,
        dtype=str
    )
    # 2) Clean header names
    df.columns = df.columns.str.strip()
    # 3) Rename first two cols
    df = df.rename(columns={df.columns[0]: "series_code", df.columns[1]: "series_name"})
    # 4) Build 'country' column by detecting header rows
    df["country"] = None
    current = None
    for i, row in df.iterrows():
        code, name = row["series_code"], row["series_name"]
        if pd.isna(code) or name.strip().lower() == "production":
            # header row: country label sits in previous row's series_name
            if i>0:
                current = df.at[i-1, "series_name"].strip()
        df.at[i, "country"] = current or "World"
    # 5) Drop the header rows
    df = df[~((df["series_name"] == df["country"]) | (df["series_name"].str.strip().str.lower() == "production"))]
    # 6) Detect year columns
    years = [c for c in df.columns if re.fullmatch(r"\d{4}", c)]
    # 7) Melt to long form
    long = df.melt(
        id_vars=["country", "series_name"],
        value_vars=years,
        var_name="year",
        value_name="production_mbpd"
    )
    long["year"] = long["year"].astype(int)
    long["production_mbpd"] = pd.to_numeric(long["production_mbpd"], errors="coerce")
    return long

df = load_data()

# Dropdown of countries
countries = ["World"] + sorted([c for c in df["country"].unique() if pd.notna(c) and c!="World"])
sel = st.selectbox("Select Country", countries)

sub = df[df["country"] == sel]

if sub.empty:
    st.warning(f"No data for {sel}.")
    st.stop()

# Plot
fig = px.line(
    sub,
    x="year", y="production_mbpd",
    color="series_name",
    title=f"{sel}: Petroleum & Liquids Production (1973–2023)",
    labels={
        "year": "Year",
        "production_mbpd": "Production (Mb/d)",
        "series_name": "Category"
    },
    markers=True
)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# Narrative
with st.expander("📌 Narrative"):
    st.markdown(f"""
    **{sel}** shows these production series over time:
    - **Total petroleum and other liquids**  
    - **Crude oil, NGPL, and other liquids**  
    - **Crude oil including lease condensate**  
    Watch for oil‐shock dips in the 1970s, rapid growth in the 2000s, and recent plateaus.
    """)

# Data Source
with st.expander("📊 Data Source"):
    st.markdown("""
    - File: `data/INT-Export-04-03-2025_21-40-52.xlsx`  
    - Parsed by detecting “country” header rows followed by “Production” blocks.  
    - Melted years 1973–2023 into long form for plotting.
    """)
