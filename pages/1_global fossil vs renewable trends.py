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
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(
            uploaded_file,
            skiprows=1,
            header=0,
            dtype=str
        )

        df.columns = df.columns.str.strip()
        df = df.rename(columns={df.columns[0]: "series_code", df.columns[1]: "series_name"})

        df['country'] = None
        current_country = "World"

        for index, row in df.iterrows():
            if pd.isna(row['series_code']) or (isinstance(row['series_name'], str) and row['series_name'].strip() == "Production"):
                if index > 0 and pd.isna(row['series_code']):
                    current_country = df.iloc[index-1]['series_name'].strip()
                elif isinstance(row['series_name'], str) and row['series_name'].strip() == "Production":
                    if index > 0:
                        current_country = df.iloc[index-1]['series_name'].strip()
                elif isinstance(row['series_name'], str) and row['series_name'].strip() == "World":
                    current_country = "World"
                elif index > 0 and isinstance(df.iloc[index-1]['series_name'], str) and df.iloc[index-1]['series_name'].strip() == "World" and \
                     isinstance(row['series_name'], str) and row['series_name'].strip() == "Production":
                    current_country = "World"

            df.at[index, 'country'] = current_country

        df = df[~((df['series_name'].isin(df['country'].unique())) | (df['series_name'].str.strip() == "Production"))]

        year_cols = [col for col in df.columns if re.fullmatch(r"\d{4}", str(col))]

        df_long = df.melt(
            id_vars=["series_code", "series_name", "country"],
            value_vars=year_cols,
            var_name="year",
            value_name="value"
        )

        df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce")
        df_long = df_long.dropna(subset=['year'])
        df_long["year"] = df_long["year"].astype(int)
        df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")

        df_long["series_name"] = df_long["series_name"].str.strip()
        df_long["country"] = df_long["country"].str.strip()

        return df_long
    else:
        return pd.DataFrame()

st.sidebar.header("Upload Data File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    df = load_data(uploaded_file)

    if df.empty or df["year"].isnull().all():
        st.error("No valid data could be processed from the uploaded file. Please check the file format and content.")
        st.stop()

    min_year, max_year = int(df["year"].min()), int(df["year"].max())

    st.title("Global Energy Production Trends Analysis")
    st.markdown("""
    Explore various energy production metrics across different countries and over time.
    """)

    st.sidebar.header("Filter Options")

    all_countries = ["All Countries"] + sorted(df["country"].unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", all_countries)

    if selected_country == "All Countries":
        available_series = sorted(df["series_name"].unique().tolist())
    else:
        available_series = sorted(df[df["country"] == selected_country]["series_name"].unique().tolist())

    default_selected_series = []
    preferred_defaults = [
        "Total petroleum and other liquids (Mb/d)",
        "Crude oil, NGPL, and other liquids (Mb/d)",
        "Crude oil including lease condensate (Mb/d)"
    ]
    for series in preferred_defaults:
        if series in available_series:
            default_selected_series.append(series)

    selected_series = st.sidebar.multiselect(
        "Select Series (multiple can be chosen)",
        available_series,
        default=default_selected_series
    )

    year_range = st.sidebar.slider(
        "Select Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    if selected_country != "All Countries":
        filtered_df = filtered_df[filtered_df["country"] == selected_country]

    if selected_series:
        filtered_df = filtered_df[filtered_df["series_name"].isin(selected_series)]
    else:
        st.warning("Please select at least one series to display the chart.")
        filtered_df = pd.DataFrame()

    if not filtered_df.empty:
        st.subheader(f"Production Trends for {selected_country} ({year_range[0]} - {year_range[1]})")

        fig = px.line(
            filtered_df,
            x="year",
            y="value",
            color="series_name",
            line_dash="country" if selected_country == "All Countries" else None,
            title="Energy Production Over Time",
            labels={"value": "Mb/d", "year": "Year", "series_name": "Series"},
            hover_data={"country": True, "value": ":.2f"}
        )
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

        if selected_country == "All Countries" and selected_series:
            st.subheader(f"Top Countries for {selected_series[0]} (Average Production)")
            avg_production_df = filtered_df[filtered_df['series_name'] == selected_series[0]]
            if not avg_production_df.empty:
                avg_production = avg_production_df.groupby('country')['value'].mean().sort_values(ascending=False).reset_index()
                top_n = st.slider("Show Top N Countries", 5, min(20, len(avg_production)), 10)
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
                st.info(f"No data to calculate top countries for '{selected_series[0]}' with current filters.")
    else:
        st.info("No data available for the selected filters. Please adjust your selections.")

    with st.expander("🔍 View Raw Data"):
        st.dataframe(filtered_df)

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
        - This app expects a CSV file similar to `INT-Export-04-03-2025_21-40-52.xlsx - Worksheet.csv`.
        - The original CSV file should have a metadata row (skipped) followed by a header row with years.
        - Data is expected to be organized by country, with various series listed under each country's "Production" header.
        """)
else:
    st.info("Please upload a CSV file to begin the analysis using the 'Upload Data File' section in the sidebar.")
