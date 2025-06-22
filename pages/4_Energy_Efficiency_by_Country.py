import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    layout="wide",
    page_title="Global Petroleum Production",
    page_icon="🛢️",
    initial_sidebar_state="expanded"
)

# Load data
@st.cache_data
def load_data():
    # Load dataset from GitHub (update URL if needed)
    url = "https://raw.githubusercontent.com/your-username/your-repo/main/data/INT-Export-04-03-2025_21-40-52.xlsx" 
    
    # Read Excel file (adjust skiprows based on your data's header structure)
    df = pd.read_excel(url, skiprows=4, header=[0, 1])
    
    # Flatten hierarchical columns
    df.columns = ["_".join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
    
    # Melt years into a single column
    country_col = [col for col in df.columns if "Country" in col][0]
    year_cols = [col for col in df.columns if col.isdigit() and 1973 <= int(col) <= 2023]
    
    melted = df.melt(id_vars=[country_col], value_vars=year_cols, var_name="Year", value_name="Production")
    melted = melted.rename(columns={country_col: "Country"})
    
    # Clean data
    melted["Year"] = melted["Year"].astype(int)
    melted["Production"] = pd.to_numeric(melted["Production"], errors="coerce")
    melted = melted.dropna(subset=["Country", "Production"])
    
    # Extract production type (e.g., "Crude Oil", "Total Petroleum") from column names
    melted["Production_Type"] = melted["Country"].str.split("_").str[1]
    melted["Country"] = melted["Country"].str.split("_").str[0]
    
    return melted

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filters")
selected_type = st.sidebar.selectbox("Select Production Type", df["Production_Type"].unique())
selected_year = st.sidebar.slider("Select Year", 1973, 2023, 2023)
top_n = st.sidebar.slider("Top N Countries", 5, 20, 10)

# Filtered data
filtered_df = df[df["Production_Type"] == selected_type]

# Dashboard layout
st.title("🛢️ Global Petroleum Production Explorer (1973–2023)")
st.markdown("Visualize production trends by country and production type")

# Top Producers Bar Chart
st.subheader(f"Top {top_n} Producers in {selected_year}")
year_df = filtered_df[filtered_df["Year"] == selected_year].sort_values("Production", ascending=False).head(top_n)
fig1 = px.bar(
    year_df,
    x="Country",
    y="Production",
    color="Country",
    title=f"{selected_type} Production in {selected_year}",
    labels={"Production": "Thousand Barrels per Day", "Country": ""}, 
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig1, use_container_width=True)

# Line Chart for Selected Countries
st.subheader(f"{selected_type} Production Over Time")
country_options = sorted(filtered_df["Country"].unique())
selected_countries = st.multiselect(
    "Select Countries", 
    country_options, 
    default=["United States", "Russia", "Saudi Arabia"]
)
time_df = filtered_df[filtered_df["Country"].isin(selected_countries)]
fig2 = px.line(
    time_df,
    x="Year",
    y="Production",
    color="Country",
    title=f"{selected_type} Production Trends",
    labels={"Production": "Thousand Barrels per Day", "Year": ""},
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig2, use_container_width=True)

# Data Table
with st.expander("📊 View Raw Data"):
    st.dataframe(
        filtered_df.pivot(index="Year", columns="Country", values="Production"),
        use_container_width=True
    )

# Download Button
st.download_button(
    "📥 Download Filtered Data",
    filtered_df.to_csv(index=False),
    "petroleum_production.csv"
)

# Insights
with st.expander("💡 Key Insights"):
    st.markdown("""
    - **Historical Shifts**: Post-1980 decline in USSR production, rise of unconventional oil (e.g., US shale).
    - **OPEC Dominance**: Saudi Arabia's crude oil production has consistently ranked in the top 3 since 1980.
    - **Natural Gas Liquids**: Rapid growth since 2010, driven by US fracking technology.
    """)
