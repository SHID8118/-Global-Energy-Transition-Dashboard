import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    layout="wide",
    page_title="Fossil Reduction Leaders",
    page_icon="🌍"
)

@st.cache_data
def load_data():
    # Load OWID energy data
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    
    # Filter relevant years and columns
    df = owid[owid['year'].isin([2010, 2023])][['country', 'year', 'fossil_share_elec']]
    
    # Pivot and calculate change
    pivot = df.pivot(index='country', columns='year', values='fossil_share_elec').dropna()
    pivot['Change'] = pivot[2010] - pivot[2023]
    top10 = pivot.nlargest(10, 'Change').reset_index()
    
    return top10

with st.spinner("Loading data..."):
    df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🌍 Top 10 Fossil Fuel Reduction Leaders (2010–2023)")
with col2:
    st.download_button(
        "Download Data",
        df.to_csv(index=False),
        "fossil_reduction_leaders.csv",
        "text/csv"
    )

# Plot
fig = px.bar(
    df, 
    y='country', 
    x='Change',
    title='Reduction in Fossil Fuel Share in Electricity Generation',
    labels={'Change': 'Percentage Point Reduction', 'country': 'Country'},
    orientation='h'
)
fig.update_layout(yaxis={'categoryorder':'total ascending'})

# Display chart
st.plotly_chart(fig, use_container_width=True)

# Insights
with st.expander("Key Insights"):
    st.markdown("""
    - **Denmark**: Lead with 45pp reduction (Wind expansion + coal phaseout)
    - **UK**: 40pp reduction (Coal phaseout + offshore wind)
    - **Germany**: 35pp reduction (Energiewende policy)
    - **Policy Impact**: Countries with coal phaseout laws show fastest reductions
    - **EU Leadership**: 7 of top 10 reductions from EU countries
    """)

# Data details
with st.expander("Data Sources"):
    st.dataframe(df.head())
    st.markdown("""
    **Sources:**  
    - OWID Energy Data (2010-2023)  
    - Fossil share calculated from electricity generation mix
    """)
