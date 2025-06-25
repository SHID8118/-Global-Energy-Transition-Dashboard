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
    year_cols = [c for c in df.columns if str(c).isdigit() and len(str(c)) == 4]

    # Melt to long format
    df_long = df.melt(
        id_vars=["country", "series_name"],
        value_vars=year_cols,
        var_name="year",
        value_name="production_mbpd"
    )

    df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce", downcast="integer")
    df_long["production_mbpd"] = pd.to_numeric(df_long["production_mbpd"], errors="coerce")

    df_long = df_long.dropna(subset=["production_mbpd"]).copy()
    df_long["country"] = df_long["country"].fillna("Unknown")

    return df_long

# Load the data
df = load_data()

# Dropdown for country selection
available_countries = sorted(df["country"].dropna().unique())
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
