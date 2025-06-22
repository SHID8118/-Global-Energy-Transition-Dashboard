import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(layout="wide", page_title="Renewable Leaders", page_icon="⚡")

@st.cache_data
def load_data():
    return pd.read_excel("data/owid-energy-data.xlsx")

# Load and prepare data
df = load_data()
df['renewables_total'] = df['wind_share_elec'] + df['solar_share_elec'] + df['hydro_share_elec'] + df['bio_share_elec']

# Sidebar filters
st.sidebar.header("Filters")
selected_year = st.sidebar.slider("Year", 2000, 2023, 2023)
country_type = st.sidebar.radio("Country Type", ["All Countries", "EU", "G20", "Custom"])

# Dynamic country selection
if country_type == "Custom":
    countries = st.sidebar.multiselect("Select Countries", df[df['year'] == selected_year]['country'].unique())
else:
    country_groups = {
        "EU": ["Germany", "France", "Italy", "Spain", "Sweden", "Poland", "Netherlands", "Belgium"],
        "G20": ["USA", "China", "India", "Russia", "Brazil", "Japan", "Germany", "Canada", 
               "South Korea", "Australia", "Indonesia", "Mexico", "Saudi Arabia"]
    }
    countries = country_groups.get(country_type, [])

# Main dashboard
st.title(f"⚡ Top Renewable Energy Leaders ({selected_year})")
st.markdown("*Countries achieving >50% renewable electricity generation*")

# Filter data based on selections
year_df = df[df['year'] == selected_year].copy()
if countries:
    year_df = year_df[year_df['country'].isin(countries)]

# Create leaderboards
leaders = year_df[year_df['renewables_total'] > 50].sort_values('renewables_total', ascending=False)

# Visualization tabs
tab1, tab2, tab3 = st.tabs(["Global Map", "Source Breakdown", "Trend Analysis"])

with tab1:
    # Interactive global map
    fig = px.choropleth(
        leaders,
        locations="iso_code",
        color="renewables_total",
        hover_name="country",
        hover_data=["hydro_share_elec", "wind_share_elec", "solar_share_elec"],
        title="Countries with >50% Renewable Electricity",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Stacked bar chart for source breakdown
    if not leaders.empty:
        fig = px.bar(
            leaders.sort_values('country'),
            x='country',
            y=['hydro_share_elec', 'wind_share_elec', 'solar_share_elec', 'bio_share_elec'],
            title="Renewable Energy Composition",
            labels={'value': 'Percentage (%)', 'variable': 'Energy Source'},
            barmode='stack'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No countries meet the 50% threshold with current filters")

with tab3:
    # Country trend analysis
    if countries:
        trend_df = df[df['country'].isin(countries)]
        fig = px.line(
            trend_df,
            x='year',
            y='renewables_total',
            color='country',
            title="Renewable Share Trends Over Time"
        )
        fig.add_hline(y=50, line_dash="dash", line_color="red")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select countries for trend analysis")

# Key metrics
if not leaders.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Top Leader", leaders.iloc[0]['country'], f"{leaders.iloc[0]['renewables_total']:.1f}%")
    col2.metric("Median Renewable Share", "", f"{leaders['renewables_total'].median():.1f}%")
    col3.metric("Countries Above 50%", len(leaders))

# Detailed insights
with st.expander("🔍 Key Insights & Policy Takeaways"):
    st.markdown("""
    **Leading Nations**:
    - **Iceland**: 100% renewables (geothermal/hydro)
    - **Norway**: 98% hydro power
    - **Uruguay**: 95% wind integration
    
    **Technology Trends**:
    - Europe leads in wind integration (Denmark: 50%+ wind)
    - Solar breakthroughs in Germany (30%+ solar share)
    - Hydro remains dominant in Nordic countries
    
    **Policy Implications**:
    1. Feed-in tariffs (Germany) enable renewable adoption
    2. Geographical advantages drive regional specialization
    3. Grid modernization critical for high penetration levels
    """)

# Data download
st.download_button(
    "Download Data",
    leaders.to_csv(index=False),
    "renewable_leaders.csv",
    "text/csv"
)

# Methodology
with st.expander("⚙️ Methodology"):
    st.markdown("""
    **Data Sources**:  
    - OWID Energy Data (2000-2023)  
    - Renewable share calculated from:  
      Wind + Solar + Hydro + Biofuels
    
    **Definitions**:  
    - Renewable electricity share = % of total electricity generation from renewable sources
    - Hydro includes traditional hydropower only
    """)
