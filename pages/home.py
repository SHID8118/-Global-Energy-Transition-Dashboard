import streamlit as st
from st_pages import Page, show_pages

# Configure page
st.set_page_config(
    layout="wide",
    page_title="Global Energy Transition Dashboard",
    page_icon="🌍"
)

# Define pages for navigation
show_pages([
    Page("pages/1_🏠_Home.py", "Home", "🏠"),
    Page("pages/2_📉_Fossil_vs_Renewables.py", "Fossil vs Renewables", "📉"),
    Page("pages/3_🌍_Fossil_Reduction_Leaders.py", "Fossil Reduction Leaders", "🌍"),
    Page("pages/4_⛽_Oil_vs_Renewables.py", "Oil vs Renewables", "⛽"),
    Page("pages/5_🌿_Renewable_Leaders.py", "Renewable Leaders", "🌿"),
    Page("pages/6_💰_Wealth_vs_Renewables.py", "Wealth vs Renewables", "💰"),
    Page("pages/7_🌪️_Renewable_Diversity.py", "Renewable Diversity", "🌪️"),
    Page("pages/8_⚙️_Energy_Industrialization.py", "Energy Industrialization", "⚙️"),
    Page("pages/9_💸_Subsidies_vs_Renewables.py", "Subsidies vs Renewables", "💸"),
    Page("pages/10_🌱_Decarbonization_Leaders.py", "Decarbonization Leaders", "🌱"),
    Page("pages/11_📈_Energy_Decoupling.py", "Energy Decoupling", "📈"),
    Page("pages/12_🎯_Net_Zero_Targets.py", "Net Zero Targets", "🎯"),
    Page("pages/13_🚧_COP28_Gap.py", "COP28 Gap", "🚧"),
    Page("pages/14_🔥_Oil_Concentration.py", "Oil Concentration", "🔥"),
    Page("pages/15_🛑_Petrostate_Transition.py", "Petrostate Transition", "🛑"),
    Page("pages/16_📊_Renewable_Tipping_Points.py", "Renewable Tipping Points", "📊"),
    Page("pages/17_🦠_COVID_Energy_Impact.py", "COVID Energy Impact", "🦠"),
    Page("pages/18_🏜️_Energy_Justice.py", "Energy Justice", "🏜️"),
    Page("pages/19_⚖️_HDI_Electricity.py", "HDI Electricity Link", "⚖️")
])

# Title and description
st.title("🌍 Global Energy Transition Dashboard")
st.markdown("""
### Explore 18 Key Questions About Energy Trends
*Data Sources: OWID, BP Statistical Review, Ember, IEA, UN SDG7, World Bank*
""")

# Dynamic dropdown with all 18 questions
questions = {
    "2": "📉 How have fossil fuels changed vs renewables since 2000?",
    "3": "🌍 Which countries reduced fossil fuel share the most (2010–2023)?",
    "4": "⛽ Do oil-producing countries lag in renewables adoption?",
    "5": "🌿 Which countries achieved >50% renewable electricity?",
    "6": "💰 How does renewable adoption vary by GDP quintile?",
    "7": "🌪️ Which regions have the most balanced renewable portfolios?",
    "8": "⚙️ Does energy supply correlate with industrialization levels?",
    "9": "💸 Do fossil subsidies slow renewable energy growth?",
    "10": "🌱 Which regions decarbonized fastest (2000–2023)?",
    "11": "📈 Which countries decoupled GDP growth from energy use?",
    "12": "🎯 How much must renewables grow to meet net zero targets?",
    "13": "🚧 Which countries are off-track for COP28 tripling goals?",
    "14": "🔥 Is oil production becoming more concentrated?",
    "15": "🛑 Do petrostates resist renewable energy transitions?",
    "16": "📊 When did renewables surpass fossils in key countries?",
    "17": "🦠 How did COVID-19 impact global energy demand?",
    "18": "🏜️ Which poor countries have untapped renewable potential?",
    "19": "⚖️ Is electricity access strongly linked to human development?"
}

selected = st.selectbox("Jump to Question:", list(questions.values()))

# Auto-navigation
if selected:
    page_num = [k for k,v in questions.items() if v==selected][0]
    st.switch_page(f"pages/{page_num}_*.py")

# Footer with all data sources
st.sidebar.markdown("""
**Data Sources & Last Updated:**  
- **OWID Energy Data**: 2023  
- **BP Statistical Review**: 2024  
- **Ember Charts**: 2023  
- **Oil Production Data**: April 2025  
- **SDG7 Renewable Share**: 2023  
- **Total Energy Supply Data**: 2023  
- **BP Oil Demand Analysis**: 2024  
- **IEA Energy Economics**: 2023  
""")
