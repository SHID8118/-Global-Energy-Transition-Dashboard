import streamlit as st

st.set_page_config(page_title="Global Energy Insights", layout="wide")

st.title("🌍 Global Energy Transition Dashboard")
st.subheader("Explore energy‑transition questions powered by real‑world data")

# ──────────────────────────────────────────────────────────────
# Questions & page mapping (length‑safe)
# ────────────────────────────────────────────────────────────
question_page_pairs = [
    ("Which countries have reduced their fossil fuel consumption the most in the last decade?", "1_Countries_Reducing_Fossil_Consumption"),
    ("Which regions or countries show a consistent decline in oil/gas/coal demand?", "2_Regions_Declining_Oil_Gas_Coal"),
    ("How has fossil fuel demand changed globally vs. in specific countries (e.g., India, China, US)?", "3_Global_vs_Country_Demand_Change"),
    ("How have petroleum and liquid‑fuel production trends changed for individual countries (or globally) from 1973 to 2023?", "4_Petroleum_and_Liquids_Production"),
    ("How has global energy intensity (measured in MJ per unit GDP PPP) changed over time, and is the world becoming more energy efficient?", "5_Global_Energy_Intensity_vs_GDP"),
    # Removed question 6
    ("What is the trend in modern renewables consumption (SDG 7.2 goal)?", "7_SDG72_Trend"),
    ("How does renewable energy growth correlate with reduction in fossil fuels?", "8_Renewables_vs_Fossil_Reduction"),
    ("Which regions are leaders in renewables adoption?", "9_Regions_Leading_Renewables"),
    ("Which countries have reduced fossil fuel use while growing their GDP?", "10_GDP_vs_Fossil_Reduction"),
    ("What is the energy supply per unit GDP? Who is the most energy‑efficient?", "11_Energy_Supply_per_GDP"),
    ("Compare fossil fuel usage trends between developed vs. developing nations.", "12_Developed_vs_Developing_Fossil"),
    ("How does India compare to other BRICS nations in reducing fossil fuel use?", "13_India_vs_BRICS"),
    ("How far is the world from achieving a renewable‑dominant energy mix?", "16_Progress_Towards_Renewable_Mix"),
    
]

questions = [q for q, _ in question_page_pairs]
page_map = {q: p for q, p in question_page_pairs}

selected_q = st.selectbox("Choose a question to explore:", questions)
selected_page = page_map[selected_q]

# ────────────────────────────────────────────────────────────
# Direct page link
# ────────────────────────────────────────────────────────────
st.page_link(
    f"pages/{selected_page}.py",
    label="🔗 Open selected analysis page",
)
