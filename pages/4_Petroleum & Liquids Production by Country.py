import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(
    layout="wide",
    page_title="Petroleum & Liquids Production by Country",
    page_icon="🌐"
)

st.title("🌐 Petroleum & Liquids Production by Country")

st.markdown("""
Select a country (or “World”) to see how its various petroleum‐liquid production series evolved from 1973–2023.
""")

@st.cache_data
def load_data():
    # Load Excel file and skip metadata row
    df = pd.read_excel("data/INT-Export-04-03-2025_21-40-52.xlsx", skiprows=1, dtype=str)
    df.columns = [str(c).strip() for c in df.columns]  # Force headers to string

    # Rename the first two columns
    df.rename(columns={df.columns[0]: "series_code", df.columns[1]: "series_name"}, inplace=True)

    # Detect and assign country
    df["country"] = None
    current_country = None
    for i, row in df.iterrows():
        code, name = row["series_code"], row["series_name"]
        if pd.isna(code) or str(name).strip().lower() == "production":
            prev_name = df.at[i - 1, "series_name"] if i > 0 else None
            if prev_name:
                current_country = str(prev_name).strip()
        df.at[i, "country"] = current_country or "World"

    # Filter out non-data rows
    df = df[~df["series_name"].str.strip().isin(["Production"] + df["country"].unique().tolist())]

    # Detect year columns (string safe)
    year_cols = [str(c) for c in df.columns if str(c).isdigit() and len(str(c)) == 4]

    # Melt to long format
    df_long = df.melt(
        id_vars=["country", "series_name"],
        value_vars=year_cols,
        var_name="year",
        value_name="production_mbpd"
    )

    df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce", downcast="integer")
    df_long["production_mbpd"] = pd.to_numeric(df_long["production_mbpd"], errors="coerce")

    return df_long.dropna(subset=["production_mbpd"])

# Load the data
df = load_data()

# Dropdown for country selection
available_countries = sorted(df["country"].unique())
selected_country = st.selectbox("Select a Country", ["World"] + [c for c in available_countries if c != "World"])

# Filter data for selected country
filtered = df[df["country"] == selected_country]

# Display line chart
if not filtered.empty:
    fig = px.line(
        filtered,
        x="year",
        y="production_mbpd",
        color="series_name",
        title=f"{selected_country}: Petroleum-Liquid Production (Mb/d)",
        labels={
            "year": "Year",
            "production_mbpd": "Production (Mb/d)",
            "series_name": "Category"
        },
        markers=True
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data found for selected country.")

# --- Narrative and Data Source ---
with st.expander("📌 Narrative"):
    st.markdown("""
    This interactive dashboard helps analyze how petroleum and liquid fuel production has evolved globally and across individual countries.

    By selecting a specific country or the global view ("World"), users can:
    - Track historical trends in total and segmented petroleum output.
    - Observe when certain countries increased or reduced their production.
    - Compare between different petroleum liquid series such as:
        - Crude oil, NGPL, and other liquids
        - NGPL (Natural Gas Plant Liquids)
        - Refinery processing gain

    This view supports understanding shifts in production strategy, self-reliance, and energy market dynamics.
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - Source File: `INT-Export-04-03-2025_21-40-52.xlsx`
    - Data provided by International Energy Agency export (assumed structured export)
    - The file contains country-wise series for petroleum and other liquids from 1973 to 2023
    - Series include multiple petroleum-based metrics in million barrels per day (Mb/d)
    - Country segments are identified based on structure of the file (e.g., 'Production' headers)
    """)
