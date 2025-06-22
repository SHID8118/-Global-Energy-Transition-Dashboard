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
    """
    Loads and processes the energy production data from an uploaded Excel file.
    """
    if uploaded_file is not None:
        # Read the Excel file
        df = pd.read_excel(
            uploaded_file,
            dtype=str
        )
        
        # Strip column headers
        df.columns = df.columns.str.strip()

        # Rename the first two columns to meaningful names
        df.rename(columns={df.columns[0]: "series_code", df.columns[1]: "series_name"}, inplace=True)

        # Assign country name based on custom row structure
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

        # Remove header rows like country names and "Production"
        df = df[~((df['series_name'].isin(df['country'].unique())) | (df['series_name'].str.strip() == "Production"))]

        # Detect year columns (e.g., "1973", "2023")
        year_cols = [col for col in df.columns if re.fullmatch(r"\d{4}", str(col))]

        # Melt to long format
        df_long = df.melt(
            id_vars=["series_code", "series_name", "country"],
            value_vars=year_cols,
            var_name="year",
            value_name="value"
        )

        df_long["year"] = pd.to_numeric(df_long["year"], errors="coerce")
        df_long = df_long.dropna(subset=["year"])
        df_long["year"] = df_long["year"].astype(int)
        df_long["value"] = pd.to_numeric(df_long["value"], errors="coerce")
        df_long["series_name"] = df_long["series_name"].str.strip()
        df_long["country"] = df_long["country"].str.strip()

        return df_long

    return pd.DataFrame()

# --- UI ---
st.sidebar.header("Upload Excel File")
uploaded_file = st.sidebar.file_uploader("Choose an Excel (.xlsx) file", type="xlsx")

if uploaded_file:
    df = load_data(uploaded_file)

    if df.empty or df["year"].isnull().all():
        st.error("No valid data could be processed from the uploaded file. Please check the file format and content.")
        st.stop()

    min_year, max_year = int(df["year"].min()), int(df["year"].max())

    st.title("Global Energy Production Trends Analysis")
    st.markdown("Explore various energy production metrics across different countries and over time.")

    st.sidebar.header("Filter Options")

    all_countries = ["All Countries"] + sorted(df["country"].unique().tolist())
    selected_country = st.sidebar.selectbox("Select Country", all_countries)

    if selected_country == "All Countries":
        available_series = sorted(df["series_name"].unique().tolist())
    else:
        available_series = sorted(df[df["country"] == selected_country]["series_name"].unique().tolist())

    preferred_defaults = [
        "Total petroleum and other liquids (Mb/d)",
        "Crude oil, NGPL, and other liquids (Mb/d)",
        "Crude oil including lease condensate (Mb/d)"
    ]
    default_selected_series = [s for s in preferred_defaults if s in available_series]

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

    # Filter data
    filtered_df = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

    if selected_country != "All Countries":
        filtered_df = filtered_df[filtered_df["country"] == selected_country]

    if selected_series:
        filtered_df = filtered_df[filtered_df["series_name"].isin(selected_series)]
    else:
        st.warning("Please select at least one series to display the chart.")
        filtered_df = pd.DataFrame()

    # --- Visualization ---
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
            avg_production_df = filtered_df[filtered_df["series_name"] == selected_series[0]]
            if not avg_production_df.empty:
                avg_production = avg_production_df.groupby("country")["value"].mean().sort_values(ascending=False).reset_index()
                top_n = st.slider("Show Top N Countries", 5, min(20, len(avg_production)), 10)
                fig_bar = px.bar(
                    avg_production.head(top_n),
                    x="country",
                    y="value",
                    title=f"Top {top_n} Countries by Average {selected_series[0]}",
                    labels={"value": "Average Mb/d", "country": "Country"},
                    color="value",
                    color_continuous_scale=px.colors.sequential.Plasma
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info(f"No data for series '{selected_series[0]}' with current filters.")
    else:
        st.info("No data available for the selected filters. Please adjust your selections.")

    with st.expander("🔍 View Raw Data"):
        st.dataframe(filtered_df)

    with st.expander("📌 Narrative"):
        st.markdown("""
        Analyze historical energy production across countries:
        - Compare trends across petroleum, NGPL, crude oil, and others.
        - Focus on a country or view global patterns.
        - Customize year range and series.

        **Key Series Definitions:**
        - Total petroleum and other liquids (Mb/d)
        - Crude oil, NGPL, and other liquids (Mb/d)
        - Crude oil including lease condensate (Mb/d)
        - NGPL (Mb/d): Natural Gas Plant Liquids
        - Other liquids (Mb/d)
        - Refinery processing gain (Mb/d)
        """)

    with st.expander("📊 Data Source"):
        st.markdown("""
        - Upload an `.xlsx` file in the format of `INT-Export-*.xlsx`.
        - Data should include country blocks, series names, and year-wise columns (e.g., 1973–2023).
        - This app processes "Production" blocks grouped by country from the EIA export format.
        """)
else:
    st.info("Please upload an Excel `.xlsx` file using the sidebar to begin.")
