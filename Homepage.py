import streamlit as st

st.set_page_config(page_title="Global Energy Insights", layout="wide")

st.title("🌍 Global Energy Transition Dashboard")
st.subheader("Explore energy‑transition questions powered by real‑world data")

# ───────────────────────────────────────────────────────────
# Question list & page map
# ───────────────────────────────────────────────────────────
questions = [
    "Which countries have reduced their fossil fuel consumption the most in the last decade?",
    "Which regions or countries show a consistent decline in oil/gas/coal demand?",
    "How has fossil fuel demand changed globally vs. in specific countries (e.g., India, China, US)?",
    "How have petroleum and liquid‑fuel production trends changed for individual countries (or globally) from 1973 to 2023?",
    "How has global energy intensity (measured in MJ per unit GDP PPP) changed over time, and is the world becoming more energy efficient?",
    # "Which countries are improving energy efficiency in terms of energy used per unit of economic output (PPP‑adjusted)?",
    "What is the trend in modern renewables consumption (SDG 7.2 goal)?",
    "How does renewable energy growth correlate with reduction in fossil fuels?",
    "Which regions are leaders in renewables adoption?",
    "Which countries have reduced fossil fuel use while growing their GDP?",
    "What is the energy supply per unit GDP? Who is the most energy‑efficient?",
    "Compare fossil fuel usage trends between developed vs. developing nations.",
    "How does India compare to other BRICS nations in reducing fossil fuel use?",
    "How far is the world from achieving a renewable‑dominant energy mix?",
]

page_map = {
    questions[0]: "1_Countries_Reducing_Fossil_Consumption",
    questions[1]: "2_Regions_Declining_Oil_Gas_Coal",
    questions[2]: "3_Global_vs_Country_Demand_Change",
    questions[3]: "4_Petroleum_and_Liquids_Production",
    questions[4]: "5_Global_Energy_Intensity_vs_GDP",
    # questions[5]: "6_Energy_Efficiency_by_Country",
    questions[6]: "7_SDG72_Trend",
    questions[7]: "8_Renewables_vs_Fossil_Reduction",
    questions[8]: "9_Regions_Leading_Renewables",
    questions[9]: "10_GDP_vs_Fossil_Reduction",
    questions[10]: "11_Energy_Supply_per_GDP",
    questions[11]: "12_Developed_vs_Developing_Fossil",
    questions[12]: "13_India_vs_BRICS",
    questions[13]: "16_Progress_Towards_Renewable_Mix",
}

selected_q = st.selectbox("Choose a question to explore:", questions)
selected_page = page_map[selected_q]

# ───────────────────────────────────────────────────────────
# Direct page link only (removing Go to analysis button)
# ───────────────────────────────────────────────────────────
st.page_link(
    f"pages/{selected_page}.py",
    label="🔗 Open selected analysis page",
    icon="🔗"
)
