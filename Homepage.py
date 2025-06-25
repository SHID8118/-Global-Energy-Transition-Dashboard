import streamlit as st

st.set_page_config(page_title="Global Energy Insights", layout="wide")
st.title("🌍 Global Energy Transition Dashboard")
st.subheader("Explore energy transition questions based on real-world data")

questions = [
    "Which countries have reduced their fossil fuel consumption the most in the last decade?",
    "Which regions or countries show a consistent decline in oil/gas/coal demand?",
    "How has fossil fuel demand changed globally vs. in specific countries (e.g., India, China, US)?",
    "How have petroleum and liquid fuel production trends changed for individual countries (or globally) from 1973 to 2023?",
    "How has global energy intensity (measured in MJ per unit GDP PPP) changed over time, and is the world becoming more energy efficient?",
    "Which countries are improving energy efficiency in terms of energy used per unit of economic output (PPP-adjusted)?",
    "Which countries have the highest growth in renewable energy share?",
    "What is the trend in modern renewables consumption (SDG 7.2 goal)?",
    "How does renewable energy growth correlate with reduction in fossil fuels?",
    "Which regions are leaders in renewables adoption?",
    "Which countries have reduced fossil fuel use while growing their GDP?",
    "What is the energy supply per unit GDP? Who is the most energy-efficient?",
    "Is there a correlation between GDP growth and clean energy investment?",
    "Compare fossil fuel usage trends between developed vs. developing nations.",
    "How does India compare to other BRICS nations in reducing fossil fuel use?",
    "Are countries with higher renewables shares also reducing emissions faster?",
    "Which countries are on track to meet UN Sustainable Development Goal 7.2 (modern renewables)?",
    "How far is the world from achieving a renewable-dominant energy mix?",
]
question = st.selectbox("Choose a question to explore:", questions)

page_map = {
    "Which countries have reduced their fossil fuel consumption the most in the last decade?": "1_Countries_Reducing_Fossil_Consumption",
    "Which regions or countries show a consistent decline in oil/gas/coal demand?": "2_Regions_Declining_Oil_Gas_Coal",
    "How has fossil fuel demand changed globally vs. in specific countries (e.g., India, China, US)?": "3_Global_vs_Country_Demand_Change",
    "How have petroleum and liquid fuel production trends changed for individual countries (or globally) from 1973 to 2023?": "4_Petroleum & Liquids Production by Country",
    "How has global energy intensity (measured in MJ per unit GDP PPP) changed over time, and is the world becoming more energy efficient?":"5_Global_Energy_Intensity_vs_GDP.py",
     "Which countries are improving energy efficiency in terms of energy used per unit of economic output (PPP-adjusted)?":6_Global_Energy_Intensity_vs_GDP_PPP.py",

    "Which countries have the highest growth in renewable energy share?": "5_Countries_Growing_Renewables",
    "What is the trend in modern renewables consumption (SDG 7.2 goal)?": "6_SDG72_Trend",
    "How does renewable energy growth correlate with reduction in fossil fuels?": "7_Renewables_vs_Fossil_Reduction",
    "Which regions are leaders in renewables adoption?": "8_Regions_Leading_Renewables",
    "Which countries have reduced fossil fuel use while growing their GDP?": "9_GDP_vs_Fossil_Reduction",
    "What is the energy supply per unit GDP? Who is the most energy-efficient?": "10_Energy_Supply_per_GDP",
    "Is there a correlation between GDP growth and clean energy investment?": "11_Correlation_GDP_Clean_Energy",
    "Compare fossil fuel usage trends between developed vs. developing nations.": "12_Developed_vs_Developing_Fossil",
    "How does India compare to other BRICS nations in reducing fossil fuel use?": "13_India_vs_BRICS",
    "Are countries with higher renewables shares also reducing emissions faster?": "14_Renewables_vs_Emissions",
    "Which countries are on track to meet UN Sustainable Development Goal 7.2 (modern renewables)?": "15_Countries_on_Track_SDG7",
    "How far is the world from achieving a renewable-dominant energy mix?": "16_Progress_Towards_Renewable_Mix",
}

if st.button("Go to Analysis"):
    st.markdown(f"[👉 Click here to go to the selected page](./{page_map[question]})")

