import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Sector Fossil Reduction",
    page_icon="🏭"
)

st.title("🏭 What Sectors Are Driving Fossil Fuel Reduction?")

st.markdown("""
This page uses the INT-Export file to show how different fossil-fuel production categories 
(e.g. total liquids, crude & NGPL, condensate) have trended for any selected country.
""")

@st.cache_data
def load_data():
    # 1) Read Excel, skip only the metadata row
    df = pd.read_excel(
        "data/INT-Export-04-03-2025_21-40-52.xlsx",
        skiprows=1,    # Row 1 is just "Report generated on…"
        dtype=str      # Keep everything string to avoid type issues
    )
    # 2) Force all headers to plain strings, stripped
    df.columns = [str(c).strip() for c in df.columns]

    # 3) Rename first two arbitrary columns
    df = df.rename(columns={df.columns[0]: "series_code", df.columns[1]: "series_name"})

    # 4) Build a 'country' column by detecting header rows
    df["country"] = None
    current_country = None
    for idx, row in df.iterrows():
        code = row["series_code"]
        name = row["series_name"]
        # Identify rows where series_code is NaN or name == "Production"
        if pd.isna(code) or str(name).strip().lower() == "production":
            # The real country label sits in the previous 'series_name'
            prev = df.at[idx - 1, "series_name"] if idx > 0 else None
            current_country = str(prev).strip() if pd.notna(prev) else current_country
        df.at[idx, "country"] = current_country or "World"

    # 5) Drop pure-header rows (where series_name == country or == "Production")
    mask_header = (
        df["series_name"].str.strip().eq(df["country"]) |
        df["series_name"].str.strip().str.lower().eq("production")
    )
    df = df[~mask_header]

    # 6) Detect year columns (those whose header is all digits)
    year_cols = [c for c in df.columns if c.isdigit()]

    # 7) Melt to long form
    df_long = df.melt(
        id_vars=["country", "series_name"],
        value_vars=year_cols,
        var_name="year",
        value_name="production_mbpd"
    )
    # 8) Convert types
    df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce").astype(int)
    df_long["production_mbpd"] = pd.to_numeric(df_long["production_mbpd"], errors="coerce")

    # 9) Filter out any rows without data
    return df_long.dropna(subset=["production_mbpd"])

df = load_data()

# Country selector (unique, sorted)
countries = sorted(df["country"].unique())
sel = st.selectbox("Select Country", ["World"] + [c for c in countries if c != "World"])

sub = df[df["country"] == sel]

if sub.empty:
    st.warning(f"No data to display for {sel}.")
    st.stop()

# Plot area chart: each series_name is a “sector” analogue
fig = px.line(
    sub,
    x="year",
    y="production_mbpd",
    color="series_name",
    title=f"{sel}: Fossil-Fuel Production by Category (Mb/d)",
    labels={
        "year": "Year",
        "production_mbpd": "Production (Mb/d)",
        "series_name": "Category"
    },
    markers=True
)
fig.update_layout(hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

with st.expander("📌 Narrative"):
    st.markdown(f"""
    - **{sel}** has the following production categories:
      - **Total petroleum and other liquids**  
      - **Crude oil, NGPL, and other liquids**  
      - **Crude oil including lease condensate**  
    - Use the dropdown above to switch between countries and inspect how each category
      has evolved from 1973 to 2023.
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - File: `data/INT-Export-04-03-2025_21-40-52.xlsx`  
    - We skip the metadata row and parse “Production” blocks per country.  
    - Melt years 1973–2023 into tidy form for plotting.
    """)
