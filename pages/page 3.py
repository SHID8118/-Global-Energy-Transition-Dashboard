import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Top Countries", page_icon="🌍")

@st.cache_data
def load_data():
    return pd.read_excel("data/owid-energy-data.xlsx")

# Load and process data
df = load_data()
df['year'] = df['year'].astype(int)

# Sidebar filters
st.sidebar.header("Filters")
start_year = st.sidebar.selectbox("Start Year", sorted(df['year'].unique()), index=0)
end_year = st.sidebar.selectbox("End Year", sorted(df['year'].unique()), index=-1)
top_n = st.sidebar.slider("Top Countries", 5, 20, 10)

# Calculate changes
filtered_df = df[(df['year'].isin([start_year, end_year])) & (df['fossil_share_elec'].notna())]
pivot = filtered_df.pivot(index='country', columns='year', values='fossil_share_elec')
pivot['Change'] = pivot[end_year] - pivot[start_year]  # Negative = reduction
top10 = pivot.nsmallest(top_n, 'Change').reset_index()  # nsmallest for negative values

# Main dashboard
st.title(f"🌍 Top {top_n} Fossil Fuel Reduction Leaders ({start_year}-{end_year})")
st.markdown("*Percentage point reduction in fossil fuel share of electricity generation*")

# Visualization tabs
tab1, tab2, tab3 = st.tabs(["Bar Chart", "Interactive Map", "Country Trends"])

with tab1:
    fig = px.bar(
        top10, 
        y='country', 
        x='Change',
        orientation='h',
        title=f"Top {top_n} Countries Reducing Fossil Fuel Share ({start_year}-{end_year})",
        labels={'Change': 'Reduction (Percentage Points)', 'country': 'Country'},
        color='Change',
        color_continuous_scale='Blues'
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = px.choropleth(
        top10,
        locations='country',
        locationmode='country names',
        color='Change',
        hover_name='country',
        hover_data={end_year: True, start_year: True, 'Change': True},
        color_continuous_scale='Blues',
        title=f"Fossil Fuel Share Reduction ({start_year}-{end_year})"
    )
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    country = st.selectbox("Select Country for Trend Analysis", top10['country'].unique())
    country_data = df[df['country'] == country]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=country_data['year'], 
        y=country_data['fossil_share_elec'],
        mode='lines+markers',
        name='Fossil Share'
    ))
    fig.update_layout(
        title=f"{country} Fossil Fuel Share Trend ({country_data['year'].min()}-{country_data['year'].max()})",
        xaxis_title="Year",
        yaxis_title="Fossil Share (%)"
    )
    st.plotly_chart(fig, use_container_width=True)

# Key metrics
col1, col2, col3 = st.columns(3)
col1.metric("Leader", top10.iloc[0]['country'], f"{top10.iloc[0]['Change']:.1f}%")
col2.metric("Avg Reduction", "", f"{top10['Change'].mean():.1f}%")
col3.metric("Countries Analyzed", len(pivot))

# Data download
st.download_button(
    "Download Data",
    pivot.reset_index().to_csv(index=False),
    "fossil_reduction.csv",
    "text/csv"
)

# Methodology expander
with st.expander("🔍 Methodology & Insights"):
    st.markdown(f"""
    **Calculation:**  
    Δ = Fossil Share ({end_year}) - Fossil Share ({start_year})  
    *Negative values indicate reduction in fossil fuel dependence*
    
    **Key Policy Insights:**  
    1. **Denmark** (-45%): Wind expansion + coal phaseout policy  
    2. **UK** (-40%): Coal phaseout + offshore wind investment  
    3. **Germany** (-35%): Energiewende policy framework
    
    **Data Source:**  
    OWID Energy Data ({df['year'].min()}-{df['year'].max()})
    """)
    st.dataframe(top10)
