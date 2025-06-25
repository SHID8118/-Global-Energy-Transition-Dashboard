import pandas as pd
import plotly.express as px

# Load data
df = pd.read_excel("Total-energy-supply-_TES_-by-source-World.xlsx", skiprows=3)

# Calculate total energy supply
energy_sources = [col for col in df.columns if col != "Year"]
df["Total"] = df[energy_sources].sum(axis=1)

# Plot energy mix over time
fig = px.area(
    df.melt(id_vars="Year", value_vars=energy_sources, var_name="Source", value_name="Production"),
    x="Year",
    y="Production",
    color="Source",
    title="Energy Supply by Source (1990–2022)",
    labels={"Production": "TJ", "Year": ""}
)
fig.show()
