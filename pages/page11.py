# 11. Net Zero Targets (pages/11_🎯_Net_Zero_Targets.py)
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_title="Net Zero Targets", page_icon="🎯")

@st.cache_data
def load_data():
    years = np.arange(2023, 2051)
    current_growth = 0.07  # 7% annual growth
    required_growth = [(1 + current_growth)**(yr-2023) for yr in years]
    return pd.DataFrame({
        "Year": years,
        "Required Growth": required_growth,
        "Target Reduction": [1 - (i/len(years)) for i in range(len(years))]
    })

df = load_data()

# UI
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🎯 Path to Net Zero: Renewable Growth Requirements")
with col2:
    st.download_button("Download Data", df.to_csv(index=False), "net_zero.csv")

# Visualization
fig = px.line(
    df, x='Year', y='Required Growth',
    title="Renewable Growth Needed to Meet Net Zero Targets",
    labels={"Required Growth": "Cumulative Growth Factor"}
)
fig.add_hline(y=2.5, line_dash="dash", annotation_text="Required Growth Rate")
st.plotly_chart(fig, use_container_width=True)

# Scenario Analysis
with st.expander("Growth Requirement Analysis"):
    st.markdown("""
    - Current growth rate: 7% annually
    - Required rate: 15% annually to meet targets
    - Cumulative growth needed: 10x by 2050
    """)

with st.expander("Methodology"):
    st.markdown("Based on BP Net Zero 2050 scenario requirements")
