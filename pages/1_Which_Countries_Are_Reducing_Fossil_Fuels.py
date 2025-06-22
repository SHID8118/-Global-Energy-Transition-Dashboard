import streamlit as st

st.set_page_config(layout="wide")
st.title("Which countries have reduced their fossil fuel consumption the most in the last decade?")

st.markdown("""
This analysis highlights the countries that have made the most progress in cutting fossil fuel consumption (coal, oil, and gas) since 2010.
""")

st.markdown("### 📊 Data Source")
st.markdown("""
- **File**: `owid-energy-data.xlsx`  
- **Columns**: `country`, `year`, `coal_consumption`, `oil_consumption`, `gas_consumption`
""")

st.info("👉 Add charts and data visualizations here.")
