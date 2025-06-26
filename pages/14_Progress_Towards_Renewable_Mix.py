# pages/16_Progress_Towards_Renewable_Mix.py
"""
Dashboard: **How far is the world from achieving a renewable-dominant energy mix?**

Goal: Plot global progress in renewables share over time.
Metric: `renewables_share_energy` from OWID.
Criteria: Highlight years when the share exceeds 50% (renewables-dominant).
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Renewables Share Over Time", layout="wide", page_icon="🌍")

st.title("🌍 Global Progress Towards Renewable‑Dominant Energy Mix")

@st.cache_data
def load_data(path: str = "data/owid-energy-data.xlsx"):
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower()
    world_df = df[df["country"] == "World"]
    world_df = world_df.dropna(subset=["renewables_share_energy"])
    return world_df

df = load_data()

if df.empty:
    st.error("Global (World) data not found in OWID file.")
    st.stop()

# Line chart of renewables share
over_50 = df[df["renewables_share_energy"] >= 50]
fig = px.line(
    df,
    x="year",
    y="renewables_share_energy",
    title="Renewables Share of Global Energy Consumption",
    labels={"renewables_share_energy": "Renewables Share (%)"},
    template="plotly_white"
)
fig.update_traces(mode="lines+markers")
fig.add_hline(y=50, line_dash="dot", line_color="green", annotation_text="Renewables > 50%", annotation_position="top left")

st.plotly_chart(fig, use_container_width=True)

# Latest year summary
latest = df.sort_values("year").iloc[-1]
with st.expander("📌 Insights"):
    st.markdown(f"In **{int(latest['year'])}**, renewables made up **{latest['renewables_share_energy']:.1f}%** of the world's energy.")
    if not over_50.empty:
        year = int(over_50.iloc[0]['year'])
        st.markdown(f"The world first crossed the 50% renewable threshold in **{year}**.")
    else:
        st.markdown("🌱 The world has **not yet crossed** the 50% renewable threshold.")

with st.expander("📊 Data Source"):
    st.markdown("OWID energy dataset – variable: `renewables_share_energy` (% of total energy)")
