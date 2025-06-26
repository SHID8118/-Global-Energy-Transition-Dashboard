import streamlit as st
from streamlit_extras.switch_page_button import switch_page  # helper for internal navigation

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
    "What is the trend in modern renewables consumption (SDG 7.2 goal)?",
    "How does renewable energy growth correlate with reduction in fossil fuels?",
    "Which regions are leaders in renewables adoption?",
    "Which countries have reduced fossil fuel use while growing their GDP?",
    "What is the energy supply per unit GDP? Who is the most energy-efficient?",
    "Compare fossil fuel usage trends between developed vs. developing nations.",
    "How does India compare to other BRICS nations in reducing fossil fuel use?",
    "How far is the world from achieving a renewable-dominant energy mix?",
]

question = st.selectbox("Choose a question to explore:", questions)

page_map = {
    "Which countries have reduced their fossil fuel consumption the most in the last decade?": "1_Countries_Reducing_Fossil_Consumption",
    "Which regions or countries show a consistent decline in oil/gas/coal demand?": "2_Regions_Declining_Oil_Gas_Coal",
    "How has fossil fuel demand changed globally vs. in specific countries (e.g., India, China, US)?": "3_Global_vs_Country_Demand_Change",
    "How have petroleum and liquid fuel production trends changed for individual countries (or globally) from 1973 to 2023?": "4_Petroleum_&_Liquids_Production_by_Country",
    "How has global energy intensity (measured in MJ per unit GDP PPP) changed over time, and is the world becoming more energy efficient?": "5_Global_Energy_Intensity_vs_GDP",
    "Which countries are improving energy efficiency in terms of energy used per unit of economic output (PPP-adjusted)?": "6_Global_Energy_Intensity_vs_GDP_PPP",
    "What is the trend in modern renewables consumption (SDG 7.2 goal)?": "7_SDG72_Trend",
    "How does renewable energy growth correlate with reduction in fossil fuels?": "8_Renewables_vs_Fossil_Reduction",
    "Which regions are leaders in renewables adoption?": "9_Regions_Leading_Renewables",
    "Which countries have reduced fossil fuel use while growing their GDP?": "10_GDP_vs_Fossil_Reduction",
    "What is the energy supply per unit GDP? Who is the most energy-efficient?": "11_Energy_Supply_per_GDP",
    "Compare fossil fuel usage trends between developed vs. developing nations.": "12_Developed_vs_Developing_Fossil",
    "How does India compare to other BRICS nations in reducing fossil fuel use?": "13_India_vs_BRICS",
    "How far is the world from achieving a renewable-dominant energy mix?": "16_Progress_Towards_Renewable_Mix",
}

if st.button("Go to Analysis"):
    # Navigate to the Streamlit page programmatically
    switch_page(page_map[question])
