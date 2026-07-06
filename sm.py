import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import plotly.express as px
import random

st.set_page_config(
    page_title="Electricity Consumption Analyzer",
    page_icon="⚡",
    layout="wide"
)

fake = Faker("en_IN")

# ------------------------------
# States & Cities
# ------------------------------

india = {
    "Maharashtra":["Mumbai","Pune","Nagpur","Nashik"],
    "Gujarat":["Ahmedabad","Surat","Vadodara"],
    "Karnataka":["Bangalore","Mysore","Hubli"],
    "Tamil Nadu":["Chennai","Coimbatore","Madurai"],
    "Delhi":["New Delhi"],
    "West Bengal":["Kolkata","Howrah"],
    "Uttar Pradesh":["Lucknow","Kanpur","Noida"],
    "Rajasthan":["Jaipur","Jodhpur"],
    "Madhya Pradesh":["Indore","Bhopal"],
    "Kerala":["Kochi","Trivandrum"]
}

st.title("⚡ Electricity Consumption Analyzer")
st.write("Analyze electricity usage across India.")

col1,col2,col3=st.columns(3)

with col1:
    state=st.selectbox("Select State",list(india.keys()))

with col2:
    city=st.selectbox("Select City",india[state])

with col3:
    consumer=st.selectbox(
        "Consumer Type",
        ["Household","Business"]
    )

days=30

hours=[]

consumption=[]

for d in range(days):

    for h in range(24):

        hours.append(f"Day {d+1} {h}:00")

        base=random.randint(1,6)

        if 18<=h<=22:
            base*=2

        if consumer=="Business":
            base*=1.8

        consumption.append(round(base+random.random(),2))

df=pd.DataFrame({
    "Time":hours,
    "Consumption(kWh)":consumption
})

# Metrics

total=df["Consumption(kWh)"].sum()

average=df["Consumption(kWh)"].mean()

peak=df["Consumption(kWh)"].max()

bill=total*8

carbon=total*0.82

c1,c2,c3,c4=st.columns(4)

c1.metric("Total Consumption",f"{total:.0f} kWh")
c2.metric("Average Usage",f"{average:.2f} kWh")
c3.metric("Estimated Bill",f"₹{bill:.0f}")
c4.metric("CO₂ Emission",f"{carbon:.1f} kg")

st.divider()

fig=px.line(
    df,
    x="Time",
    y="Consumption(kWh)",
    title="Electricity Consumption"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

hourly=df.copy()

hourly["Hour"]=hourly["Time"].str.extract(r'(\d+):')

hourly["Hour"]=hourly["Hour"].astype(int)

peak_hour=hourly.groupby("Hour")["Consumption(kWh)"].mean().idxmax()

st.subheader("🕒 Peak Hour Analysis")

st.success(f"Highest Consumption Hour : {peak_hour}:00")

st.divider()

st.subheader("💡 Energy Saving Suggestions")

if average>7:
    st.error("""
Use LED bulbs

Turn OFF unused appliances

Reduce AC temperature

Install Solar Panels

Use Smart Meters
""")

else:
    st.success("""
Great!

Your electricity usage is efficient.
""")

st.divider()

st.download_button(
    "Download Report",
    df.to_csv(index=False),
    file_name="electricity_report.csv"
)
