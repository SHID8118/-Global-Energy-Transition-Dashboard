# pages/8\_Renewables\_vs\_Fossil\_Reduction.py

"""
Dashboard question:
**Which countries have grown their renewable share while reducing fossil fuel use?**
This version auto‑detects columns using the OWID variable lists you supplied.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────────────────────────────────────────────────────

# Page config

# ────────────────────────────────────────────────────────────────────────────────

st.set\_page\_config(
page\_title="Renewables vs Fossils (OWID)",
layout="wide",
page\_icon="🔗"
)

st.title("🔗 Renewable Share vs Fossil Fuel Consumption")
st.markdown(
"""
Scatter plot showing the relationship between a country's **share of renewables** in total
energy consumption and its **absolute fossil‑fuel consumption** (TWh) for the latest
available year in the OWID energy dataset.
"""
)

# ────────────────────────────────────────────────────────────────────────────────

# Variable categories supplied by the user

# ────────────────────────────────────────────────────────────────────────────────

FOSSIL\_COLS = \[
"coal\_consumption", "oil\_consumption", "gas\_consumption",  # key absolute values
"fossil\_fuel\_consumption"                                     # already‑aggregated in OWID
]

RENEW\_SHARE\_COL = "renewables\_share\_energy"  # % share column from OWID

# ────────────────────────────────────────────────────────────────────────────────

# Data loader

# ────────────────────────────────────────────────────────────────────────────────

@st.cache\_data

def load\_data(path: str = "data/owid-energy-data.xlsx"):
df = pd.read\_excel(path)
\# Normalise column names
df.columns = df.columns.str.strip().str.lower()

```
if "year" not in df.columns or "country" not in df.columns:
    st.error("Required columns 'year' or 'country' are missing from the dataset.")
    st.stop()

# Latest year with non‑NA renewables share
df_valid = df[df[RENEW_SHARE_COL].notna()]
latest_year = int(df_valid["year"].max())
df_latest = df_valid[df_valid["year"] == latest_year].copy()

# Ensure fossil columns exist; if not, fall back to 'fossil_fuel_consumption'
for col in FOSSIL_COLS:
    if col not in df_latest.columns:
        df_latest[col] = pd.NA

# Calculate total fossil consumption: use OWID's aggregated value if present,
# otherwise sum coal/oil/gas
if df_latest["fossil_fuel_consumption"].notna().any():
    df_latest["fossil_total"] = df_latest["fossil_fuel_consumption"]
else:
    df_latest["fossil_total"] = df_latest[[
        "coal_consumption", "oil_consumption", "gas_consumption"
    ]].sum(axis=1, skipna=True)

df_latest = df_latest[["country", RENEW_SHARE_COL, "fossil_total"]].dropna()
return df_latest, latest_year
```

# ────────────────────────────────────────────────────────────────────────────────

# Load data

# ────────────────────────────────────────────────────────────────────────────────

df, year = load\_data()

# ────────────────────────────────────────────────────────────────────────────────

# Country selector

# ────────────────────────────────────────────────────────────────────────────────

all\_countries = sorted(df\["country"].unique())
select = st.multiselect(
"Select countries (default: all)",
options=all\_countries,
default=all\_countries
)
plot\_df = df\[df\["country"].isin(select)] if select else df

# ────────────────────────────────────────────────────────────────────────────────

# Scatter plot

# ────────────────────────────────────────────────────────────────────────────────

fig = px.scatter(
plot\_df,
x=RENEW\_SHARE\_COL,
y="fossil\_total",
hover\_name="country",
title=f"Renewables Share vs Fossil Consumption – {year}",
labels={
RENEW\_SHARE\_COL: "Renewables Share in Energy (%)",
"fossil\_total": "Fossil Consumption (TWh)"
},
color=RENEW\_SHARE\_COL,
size="fossil\_total",
height=600,
template="plotly\_white"
)
fig.update\_traces(marker=dict(line=dict(width=1, color="DarkSlateGrey"), opacity=0.8))
fig.update\_layout(hovermode="closest")

st.plotly\_chart(fig, use\_container\_width=True)

# ────────────────────────────────────────────────────────────────────────────────

# Narrative & data source

# ────────────────────────────────────────────────────────────────────────────────

with st.expander("📌 Key Insights"):
st.markdown(
"""
\- **Upper‑left corner** → high renewables share, low fossil use – the desired transition path.
\- **Lower‑right corner** → low renewables share, high fossil use – lagging in the transition.
\- Hover over points for exact values. Use the multiselect to focus on specific countries.
"""
)

with st.expander("📊 Data Source"):
st.markdown(
"""
\- **Dataset:** `owid-energy-data.xlsx` (Our World in Data)
\- **Variables used:** `renewables_share_energy`, `fossil_fuel_consumption` (or sum of coal/oil/gas)
\- **Year displayed:** {year}
"""
)
