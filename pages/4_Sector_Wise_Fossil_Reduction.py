import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    page_title="Sector Fossil Reduction",
    page_icon="🏭"
)

@st.cache_data
def load_data():
    # Try loading your sector-specific file
    path = "data/INT-Export-04-03-2025_21-40-52.xlsx"
    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    
    # Identify year column
    year_col = next((col for col in df.columns if "year" in col), None)
    if year_col is None:
        st.error("No year column found in sector dataset.")
        return None, None
    
    # Possible sector names
    sectors = ["transport", "industry", "power", "electricity"]
    # Find which of these exist
    present = [col for col in sectors if col in df.columns]
    if not present:
        st.warning(f"No sector columns found. Available columns: {df.columns.tolist()}")
        return df, None
    
    # Keep only year + present sectors
    df_clean = df[[year_col] + present].rename(columns={year_col: "year"})
    return df_clean, present

df, sectors = load_data()

st.title("What sectors are driving fossil fuel reduction?")
st.markdown("""
Area chart of fossil fuel consumption by sector.  
If your sector file includes Transport, Industry, or Power data, they will be displayed below.
""")

if df is None:
    st.stop()

if not sectors:
    st.info("Please provide a sector-specific dataset with columns like 'transport', 'industry', 'power'.")
else:
    # Plot area chart
    fig = px.area(
        df,
        x="year",
        y=sectors,
        title="Sector-wise Fossil Consumption Over Time",
        labels={"value": "Consumption (TWh)", "year": "Year", "variable": "Sector"}
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("📌 Narrative"):
    st.markdown("""
    - The sector(s) shown above indicate where fossil reductions are most pronounced.  
    - For example, declines in power generation reflect renewable replacements; transport may lag.
    """)

with st.expander("📊 Data Source"):
    st.markdown(f"""
    - `data/INT-Export-04-03-2025_21-40-52.xlsx`  
    - Columns used: `year` + {sectors if sectors else 'N/A'}
    """)
