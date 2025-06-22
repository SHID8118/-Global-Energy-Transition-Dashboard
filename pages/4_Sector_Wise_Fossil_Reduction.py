import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(
    layout="wide",
    page_title="Global Energy Production Trends",
    page_icon="⛽"
)

@st.cache_data
def load_data():
    # 1) Read sheet, skipping the first metadata row
    df = pd.read_excel(
        "data/INT-Export-04-03-2025_21-40-52.xlsx",
        skiprows=1,        # skip the "Report generated on..." row
        header=0,          # use the next row as header
        dtype=str
    )
    # 2) Clean header names
    df.columns = df.columns.str.strip()
    # 3) Rename the first two columns into meaningful names
    df = df.rename(columns={df.columns[0]: "series_code", df.columns[1]: "series_name"})

    # Extract country names and series names
    # Country names are in 'series_name' where 'series_code' is NaN or 'Production'
    # We'll use a forward fill strategy to assign country names to their respective series
    df['country'] = None
    current_country = "World" # Default for the first block

    for index, row in df.iterrows():
        if pd.isna(row['series_code']) or row['series_name'] == "Production":
            current_country = df.iloc[index-1]['series_name'] if index > 0 and pd.isna(row['series_code']) else "World"
            if row['series_name'] == "Production": # If 'Production' is explicitly mentioned, the country is the one before it
                current_country = df.iloc[index-1]['series_name']
        df.at[index, 'country'] = current_country

    # Filter out rows that are just country headers or 'Production' headers
    df = df[~((df['series_name'].isin(df['country'].unique())) | (df['series_name'] == "Production"))]

    # 4) Detect year columns: any column whose header is exactly 4 digits
    year_cols = [col for col in df.columns if re.fullmatch(r"\d{4}", str(col))]

    # 5) Melt to long format
    df_long = df.melt(
        id_vars=["series_code", "series_name", "country"],
        value_vars=year_cols,
        var_name="year",
        value_name="value"
    )
    # 6) Convert types
    df_long["year"] = df_long["year"].astype(int)
    df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")

    # Clean up series names - remove leading/trailing spaces
    df_long["series_name"] = df_long["series_name"].str.strip()

    return df_long

df = load_data()

st.title("Global Energy Production Trends Analysis")
st.markdown("""
Explore various energy production metrics across different countries and over time.
""")

# --- Sidebar for Filters ---
st.sidebar.header("Filter Options")

# Country selection
all_countries = ["All Countries"] + sorted(df["country"].unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", all_countries)

# Series selection
# Get unique series names based on the selected country
if selected_country == "All Countries":
    available_series = sorted(df["series_name"].unique().tolist())
else:
    available_series = sorted(df[df["country"] == selected_country]["series_name"].unique().tolist())

selected_series = st.sidebar.multiselect(
    "Select Series (multiple can be chosen)",
    available_series,
    default=[
        "Total petroleum and other liquids (Mb/d)",
        "Crude oil, NGPL, and other liquids (Mb/d)",
        "Crude oil including lease condensate (Mb/d)"
    ] if "Total petroleum and other liquids (Mb/d)" in available_series else [] # Default if available
)

# Year range slider
min_year, max_year = int(df["year"].min()), int(df["year"].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# --- Data Filtering ---
filtered_df = df[
    (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])
]

if selected_country != "All Countries":
    filtered_df = filtered_df[filtered_df["country"] == selected_country]

if selected_series:
    filtered_df = filtered_df[filtered_df["series_name"].isin(selected_series)]
else:
    st.warning("Please select at least one series to display the chart.")
    filtered_df = pd.DataFrame() # Empty dataframe to prevent chart errors

# --- Visualizations ---
if not filtered_df.empty:
    st.subheader(f"Production Trends for {selected_country} ({year_range[0]} - {year_range[1]})")

    fig = px.line(
        filtered_df,
        x="year",
        y="value",
        color="series_name",
        line_dash="country" if selected_country == "All Countries" else None, # Differentiate by country if 'All Countries'
        title="Energy Production Over Time",
        labels={"value": "Mb/d", "year": "Year", "series_name": "Series"},
        hover_data={"country": True, "value": ":.2f"}
    )
    fig.update_layout(hovermode="x unified") # For better hover experience
    st.plotly_chart(fig, use_container_width=True)

    # If 'All Countries' is selected, show top N countries for a selected series
    if selected_country == "All Countries" and selected_series:
        st.subheader(f"Top Countries for {selected_series[0]} (Average Production)")
        # Calculate average production for the first selected series
        avg_production = filtered_df[filtered_df['series_name'] == selected_series[0]].groupby('country')['value'].mean().sort_values(ascending=False).reset_index()
        top_n = st.slider("Show Top N Countries", 5, 20, 10)
        fig_bar = px.bar(
            avg_production.head(top_n),
            x="country",
            y="value",
            title=f"Top {top_n} Countries by Average {selected_series[0]} ({year_range[0]} - {year_range[1]})",
            labels={"value": "Average Mb/d", "country": "Country"},
            color="value",
            color_continuous_scale=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.info("No data available for the selected filters. Please adjust your selections.")


# --- Raw Data Display (Optional) ---
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered_df)

# --- Narrative and Data Source ---
with st.expander("📌 Narrative"):
    st.markdown("""
    This interactive dashboard allows you to analyze global energy production trends.
    You can filter the data by country, specific energy series, and year range to gain insights into:
    - **Historical production patterns:** Observe how different energy sources have evolved over time.
    - **Country-specific trends:** Understand the production landscape of individual nations.
    - **Comparative analysis:** Compare the production of different energy series or countries.

    **Key Series Definitions:**
    - **Total petroleum and other liquids (Mb/d):** Represents the broadest measure, including all liquids from various sources.
    - **Crude oil, NGPL, and other liquids (Mb/d):** Tracks upstream production before extensive processing.
    - **Crude oil including lease condensate (Mb/d):** Focuses on the pure oil component, including lease condensate.
    - **NGPL (Mb/d):** Natural Gas Plant Liquids.
    - **Other liquids (Mb/d):** Catch-all for other liquid fuels.
    - **Refinery processing gain (Mb/d):** Represents the increase in volume of petroleum products produced by refineries compared to the crude oil and other inputs.
    """)

with st.expander("📊 Data Source"):
    st.markdown("""
    - `INT-Export-04-03-2025_21-40-52.xlsx`
    - The original Excel file has a metadata row (skipped) followed by a header row with years.
    - Data is organized by country, with various series listed under each country's "Production" header.
    """)
