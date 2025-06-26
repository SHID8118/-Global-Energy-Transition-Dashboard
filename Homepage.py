import streamlit as st
from streamlit\_extras.switch\_page\_button import switch\_page  # helper for internal navigation

st.set\_page\_config(page\_title="Global Energy Insights", layout="wide")
st.title("🌍 Global Energy Transition Dashboard")
st.subheader("Explore energy transition questions based on real-world data")

questions = \[
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

page\_map = {
"Which countries have reduced their fossil fuel consumption the most in the last decade?": "1\_Countries\_Reducing\_Fossil\_Consumption",
"Which regions or countries show a consistent decline in oil/gas/coal demand?": "2\_Regions\_Declining\_Oil\_Gas\_Coal",
"How has fossil fuel demand changed globally vs. in specific countries (e.g., India, China, US)?": "3\_Global\_vs\_Country\_Demand\_Change",
"How have petroleum and liquid fuel production trends changed for individual countries (or globally) from 1973 to 2023?": "4\_Petroleum & Liquids Production by Country",
"How has global energy intensity (measured in MJ per unit GDP PPP) changed over time, and is the world becoming more energy efficient?": "5\_Global\_Energy\_Intensity\_vs\_GDP.py",
"Which countries are improving energy efficiency in terms of energy used per unit of economic output (PPP-adjusted)?": "6\_Global\_Energy\_Intensity\_vs\_GDP\_PPP.py",
"What is the trend in modern renewables consumption (SDG 7.2 goal)?": "7\_SDG72\_Trend",
"How does renewable energy growth correlate with reduction in fossil fuels?": "8\_Renewables\_vs\_Fossil\_Reduction",
"Which regions are leaders in renewables adoption?": "9\_Regions\_Leading\_Renewables",
"Which countries have reduced fossil fuel use while growing their GDP?": "10\_GDP\_vs\_Fossil\_Reduction",
"What is the energy supply per unit GDP? Who is the most energy-efficient?": "11\_Energy\_Supply\_per\_GDP",
"Compare fossil fuel usage trends between developed vs. developing nations.": "12\_Developed\_vs\_Developing\_Fossil",
"How does India compare to other BRICS nations in reducing fossil fuel use?": "13\_India\_vs\_BRICS",
"How far is the world from achieving a renewable-dominant energy mix?": "16\_Progress\_Towards\_Renewable\_Mix",
}

if st.button("Go to Analysis"):
\# Navigate to the Streamlit page programmatically
switch\_page(page\_map\[question])
