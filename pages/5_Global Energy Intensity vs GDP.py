import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    try:
        # Read Excel files with correct skiprows
        source_df = pd.read_excel("data/Total-energy-supply-_TES_-by-source-World.xlsx", skiprows=3)
        gdp_df = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-World.xlsx", skiprows=3)
        gdp_ppp_df = pd.read_excel("data/Total-energy-supply-_TES_-by-GDP-_PPP_-World.xlsx", skiprows=3)

        # Safely drop Units column if it exists
        if "Units" in source_df.columns:
            source_df = source_df.drop(columns=["Units"])
        if "Units" in gdp_df.columns:
            gdp_df = gdp_df.drop(columns=["Units"])
        if "Units" in gdp_ppp_df.columns:
            gdp_ppp_df = gdp_ppp_df.drop(columns=["Units"])

        # Merge datasets
        df = source_df.merge(gdp_df, on="Year", how="inner")
        df = df.merge(gdp_ppp_df, on="Year", how="inner")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

df = load_data()
st.success("Data loaded successfully!")
st.dataframe(df.head())
