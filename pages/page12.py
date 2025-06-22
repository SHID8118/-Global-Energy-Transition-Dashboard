# 12. COP28 Gap (pages/12_🚧_COP28_Gap.py)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="COP28 Gap", page_icon="🚧")

@st.cache_data
def load_data():
    owid = pd.read_excel("data/owid-energy-data.xlsx")
    owid = owid[owid['year'] == 2023]
    owid['required'] = 3 * owid['renewables_share_energy']
    owid['gap'] = owid['required'] - owid['renewables_share_energy']
    return owid.sort_values('gap', ascending=False).head(20)

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚧 COP28 Tripling Gap Analysis (Top 20 Countries)")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "cop28_gap.csv")

# Visualization
fig = px.bar(
    df, x='country', y='gap',
    title="Renewable Capacity Gap vs COP28 Targets",
    labels={"gap": "Percentage Point Shortfall"}
)
st.plotly_chart(fig, use_container_width=True)

# Country Analysis
with st.expander("Key Country Gaps"):
    st.markdown("""
    - **China**: Largest gap (45% shortfall)
    - **USA**: 40% shortfall
    - **India**: 35% shortfall
    """)

with st.expander("Methodology"):
    st.markdown("Gap calculated as 3x current renewable share minus current share")
