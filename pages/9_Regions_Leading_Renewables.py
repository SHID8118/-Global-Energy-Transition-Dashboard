# pages/8_Regions_Leading_Renewables.py
"""
Dashboard: Which regions are leaders in renewables adoption?
Using OWID energy data to aggregate the latest **renewables_share_energy** by region/continent.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────────────────────────────────────
# Page configuration
# ────────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Regions Leading Renewables Adoption",
    layout="wide",
    page_icon="🌍"
)

st.title("🌍 Regions Leading in Renewable Energy Adoption")
st.markdown(
    """
    This dashboard ranks world regions (continents) by their **share of renewables** in total
    energy consumption, using the latest year available in the OWID dataset.
    """
)

# ────────────────────────────────────────────────────────────────────────────────
# Data loader
# ────────────────────────────────────────────────────────────────────────────────
@st.cache_data

def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    # Require year, country, continent, renewables_share_energy
    needed = ["year", "country", "continent", "renewables_share_energy"]
    missing = [c for c in needed if c not in df.columns]
    if missing:
        st.error(f"Missing columns in dataset: {missing}")
        st.stop()

    # Latest year with valid renewables share
    latest_year = int(df[df["renewables_share_energy"].notna()]["year"].max())
    latest_df = df[(df["year"] == latest_year) & df["renewables_share_energy"].notna()].copy()

    # Drop aggregate entries like 'World' that have no continent value
    latest_df = latest_df.dropna(subset=["continent"])

    # Aggregate by continent (mean renewables share)
    region_df = (
        latest_df.groupby("continent", as_index=False)
        ["renewables_share_energy"].mean()
        .rename(columns={"renewables_share_energy": "avg_renewables_share"})
        .sort_values("avg_renewables_share", ascending=False)
    )
    return region_df, latest_year

# Load data
region_df, year = load_data()

# Optional multiselect to show/hide regions
selected_regions = st.multiselect(
    "Select regions to display:",
    options=region_df["continent"].tolist(),
    default=region_df["continent"].tolist()
)
plot_df = region_df[region_df["continent"].isin(selected_regions)]

# Bar chart
fig = px.bar(
    plot_df,
    x="continent",
    y="avg_renewables_share",
    title=f"Average Renewable Energy Share by Region – {year}",
    labels={"avg_renewables_share": "Renewables Share (%)", "continent": "Region"},
    color="avg_renewables_share",
    color_continuous_scale="Greens",
    height=500,
    template="plotly_white"
)
fig.update_layout(xaxis_tickangle=-30)
st.plotly_chart(fig, use_container_width=True)

# Key insights
with st.expander("📌 Key Insights"):
    st.markdown(
        """
        - Regions at the top of the bar chart have a **higher average share** of renewables in their
          energy mix.
        - Differences reflect policy, resource endowment, and investment in clean energy.
        - Hover bars to see exact percentages.
        """
    )

# Data Source
with st.expander("📊 Data Source"):
    st.markdown(
        """
        - **Dataset:** `owid-energy-data.xlsx` – Our World in Data
        - **Metric used:** `renewables_share_energy` (share of renewables in total energy)
        - **Year shown:** {year}
        - Aggregated by continent using simple mean.
        """
    )
