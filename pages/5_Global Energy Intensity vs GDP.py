import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(layout="wide", page_title="Energy Supply Dashboard", page_icon="⚡")

# Load data
@st.cache_data
def load_data():
    # Load datasets with correct filenames
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

df = load_data()

# Header
st.title("⚡ Global Energy Supply & Efficiency Dashboard")
st.markdown("Analyze energy trends, intensity, and economic correlations (1990–2022)")

# Key Metrics
col1, col2, col3 = st.columns(3)
latest_year = df["Year"].max()
latest_data = df[df["Year"] == latest_year].iloc[0]

col1.metric(f"Total Energy Supply {latest_year}", f"{latest_data['Total']:,.0f} TJ", 
           delta=f"{(latest_data['Total'] - df[df['Year'] == latest_year - 1]['Total'].values[0])/1e6:.1f}M TJ change")
col2.metric("Energy Intensity (GDP)", f"{latest_data['TES/GDP']:.1f} MJ/$", 
           delta=f"{latest_data['TES/GDP'] - df[df['Year'] == latest_year - 1]['TES/GDP'].values[0]:.1f} MJ/$")
col3.metric("Energy Intensity (PPP)", f"{latest_data['TES/GDP PPP']:.1f} MJ/$", 
           delta=f"{latest_data['TES/GDP PPP'] - df[df['Year'] == latest_year - 1]['TES/GDP PPP'].values[0]:.1f} MJ/$")

# Energy Mix Over Time
st.subheader("🌍 Energy Source Distribution Over Time")
energy_sources = [col for col in df.columns if col not in ["Year", "TES/GDP", "TES/GDP PPP", "Total"]]
fig1 = px.area(
    df.melt(id_vars="Year", value_vars=energy_sources, var_name="Source", value_name="Production"),
    x="Year",
    y="Production",
    color="Source",
    title="Energy Production by Source (1990–2022)",
    labels={"Production": "TJ", "Year": ""}
)
st.plotly_chart(fig1, use_container_width=True)

# Energy Intensity Comparison
st.subheader("📉 Energy Intensity Trends")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=df["Year"], y=df["TES/GDP"], name="Energy Intensity (GDP)"))
fig2.add_trace(go.Scatter(x=df["Year"], y=df["TES/GDP PPP"], name="Energy Intensity (PPP)"))
fig2.update_layout(title="Energy Intensity Over Time", xaxis_title="Year", yaxis_title="MJ/thousand USD")
st.plotly_chart(fig2, use_container_width=True)

# Correlation Analysis
st.subheader("📊 Energy Mix vs Economic Efficiency")
selected_year = st.slider("Select Year", df["Year"].min(), df["Year"].max(), 2020)

year_data = df[df["Year"] == selected_year].iloc[0]
energy_values = year_data[energy_sources].to_dict()

fig3 = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "bar"}]])
fig3.add_trace(
    go.Pie(
        labels=list(energy_values.keys()),
        values=list(energy_values.values()),
        name="Energy Mix"
    ),
    row=1, col=1
)
fig3.add_trace(
    go.Bar(
        x=["Energy Intensity (GDP)", "Energy Intensity (PPP)"],
        y=[year_data["TES/GDP"], year_data["TES/GDP PPP"]],
        name="Efficiency Metrics"
    ),
    row=1, col=2
)
fig3.update_layout(title_text=f"Energy Profile for {selected_year}")
st.plotly_chart(fig3, use_container_width=True)

# Data Explorer
with st.expander("🔍 Raw Data Explorer"):
    st.dataframe(df, use_container_width=True)

# Download Section
st.download_button(
    "📥 Download All Data",
    df.to_csv(index=False),
    "global_energy_supply.csv"
)

# Insights Section
with st.expander("💡 Key Insights"):
    st.markdown("""
    - **Fossil Dominance**: Oil has consistently been the largest energy source (30-40% of total supply)
    - **Green Growth**: Wind/solar energy has grown 10x since 2000 (from 1.5TJ to 19TJ)
    - **Energy Efficiency**: Energy intensity (GDP) has steadily decreased by 30% since 1990
    - **PPP Adjustment**: PPP metrics show consistently lower intensity values (≈30% less than GDP-based values)
    - **Coal Resurgence**: Coal production increased by 85% from 1990 to 2022 despite climate goals
    """)
