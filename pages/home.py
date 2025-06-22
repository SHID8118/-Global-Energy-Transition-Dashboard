import streamlit as st
from st_pages import Page, show_pages

st.set_page_config(layout="wide", page_title="🌍 Global Energy Transition Dashboard", page_icon="🌍")

show_pages([
    Page("pages/1_📉_Fossil_vs_Renewables.py", "Fossil vs Renewables", "📉"),
    Page("pages/2_🌍_Fossil_Reduction_Leaders.py", "Fossil Reduction Leaders", "🌍"),
    Page("pages/3_⛽_Oil_vs_Renewables.py", "Oil vs Renewables", "⛽"),
    Page("pages/4_🌿_Renewable_Leaders.py", "Renewable Leaders", "🌿"),
    Page("pages/5_💰_Wealth_vs_Renewables.py", "Wealth vs Renewables", "💰"),
    Page("pages/6_🌪️_Renewable_Diversity.py", "Renewable Diversity", "🌪️"),
    Page("pages/7_⚙️_Energy_Industrialization.py", "Energy Industrialization", "⚙️"),
    Page("pages/8_💸_Subsidies_vs_Renewables.py", "Subsidies vs Renewables", "💸"),
    Page("pages/9_🌱_Decarbonization_Leaders.py", "Decarbonization Leaders", "🌱"),
    Page("pages/10_📈_Energy_Decoupling.py", "Energy Decoupling", "📈"),
    Page("pages/11_🎯_Net_Zero_Targets.py", "Net Zero Targets", "🎯"),
    Page("pages/12_🚧_COP28_Gap.py", "COP28 Gap", "🚧"),
    Page("pages/13_🔥_Oil_Concentration.py", "Oil Concentration", "🔥"),
    Page("pages/14_🛑_Petrostate_Transition.py", "Petrostate Transition", "🛑"),
    Page("pages/15_📊_Renewable_Tipping_Points.py", "Renewable Tipping Points", "📊"),
    Page("pages/16_🦠_COVID_Energy_Impact.py", "COVID Energy Impact", "🦠"),
    Page("pages/17_ dessert _Energy_Justice.py", "Energy Justice", " dessert "),
    Page("pages/18_⚖️_HDI_Electricity_Link.py", "HDI Electricity Link", "⚖️")
])

st.title("🌍 Global Energy Transition Dashboard")
st.markdown("### Explore 18 Key Questions About Energy Trends")
st.markdown("*Data Sources: OWID, BP Statistical Review, Ember, IEA, UN SDG7, World Bank*")

st.sidebar.markdown("""
**Data Last Updated:**  
- OWID: 2023  
- BP: 2024  
- Ember: 2023  
- IEA: 2023  
""")
