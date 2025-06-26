# pages/9_Regions_Leading_Renewables.py
"""
Dashboard: Which regions *or* countries are leaders in renewables adoption?

* If the OWID dataset has a **`continent`** column → rank continents.
* If it does **not** → fall back to ranking **countries**.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page config
# --------------------------------------------------
st.set_page_config(
    page_title="Leaders in Renewable Adoption",
    layout="wide",
    page_icon="🌱"
)

st.title("🌱 Leaders in Renewable Energy Adoption")

# --------------------------------------------------
# Data loader
# --------------------------------------------------
@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()

    if "renewables_share_energy" not in df.columns:
        st.error("Column `renewables_share_energy` not found in the dataset.")
        st.stop()

    latest_year = int(df[df["renewables_share_energy"].notna()]["year"].max())
    latest_df = df[(df["year"] == latest_year) & df["renewables_share_energy"].notna()].copy()

    return latest_df, latest_year

# --------------------------------------------------
# Load data and determine grouping level
# --------------------------------------------------
latest_df, year = load_data()

if "continent" in latest_df.columns:
    group_mode = "continent"
    data_df = (
        latest_df.dropna(subset=["continent"])
        .groupby("continent", as_index=False)["renewables_share_energy"].mean()
        .rename(columns={"renewables_share_energy": "renew_share"})
        .sort_values("renew_share", ascending=False)
    )
else:
    group_mode = "country"
    data_df = (
        latest_df[["country", "renewables_share_energy"]]
        .rename(columns={"renewables_share_energy": "renew_share"})
        .sort_values("renew_share", ascending=False)
    )

# --------------------------------------------------
# UI controls
# --------------------------------------------------
max_n = 25 if group_mode == "country" else len(data_df)
N = st.slider("Show top N", 3, max_n, min(10, max_n))
plot_df = data_df.head(N)

# --------------------------------------------------
# Chart
# --------------------------------------------------
fig = px.bar(
    plot_df,
    x=group_mode,
    y="renew_share",
    title=f"Top {N} {group_mode.capitalize()}s by Renewable Share – {year}",
    labels={"renew_share": "Renewables Share (%)", group_mode: group_mode.capitalize()},
    color="renew_share",
    color_continuous_scale="Greens",
    height=500,
    template="plotly_white"
)
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# All data section
# --------------------------------------------------
st.subheader("Full Ranking of All Countries")
st.dataframe(data_df.reset_index(drop=True))

# --------------------------------------------------
# Insights & source
# --------------------------------------------------
with st.expander("📌 Key Insights"):
    st.markdown(
        f"""
        - The bars show which {group_mode}s have the **highest share** of renewables in their total energy mix.
        - Adjust the slider to reveal more or fewer entries.
        - Hover a bar to see the exact percentage.
        """
    )

with st.expander("📊 Data Source"):
    st.markdown(
        f"""
        - **Dataset:** `owid-energy-data.xlsx` (Our World in Data)
        - **Metric used:** `renewables_share_energy`
        - **Year displayed:** {year}
        - Grouped by **{group_mode}**.
        """
    )
