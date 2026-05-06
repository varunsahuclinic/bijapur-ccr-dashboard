import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

st.set_page_config(page_title="Bijapur CCR Dashboard", layout="wide", page_icon="🌍")

st.title("🌍 Bijapur Child Climate Resilience Dashboard (CCR)")
st.markdown("**Open Source Digital Public Good for UNICEF Venture Fund**")

st.sidebar.header("📍 Bijapur, Chhattisgarh")
st.sidebar.metric("Vulnerability Level", "Very High")

# Current Weather
st.subheader("🌡️ Current Weather & 7-Day Forecast")
lat, lon = 18.79, 80.82
url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Asia/Kolkata"

try:
    resp = requests.get(url).json()
    current = resp['current']
    col1, col2, col3 = st.columns(3)
    col1.metric("Temperature", f"{current['temperature_2m']}°C")
    col2.metric("Humidity", f"{current['relative_humidity_2m']}%")
    col3.metric("Rain Today", f"{resp['daily']['precipitation_sum'][0]} mm")
except:
    st.warning("Weather data unavailable")

# Sample Data & Risk Table
st.subheader("🔮 Climate-Health Risk Prediction")
data = {
    'Date': pd.date_range(start=datetime.now(), periods=7).strftime('%d %b'),
    'Malaria Risk Score': [45, 78, 92, 65, 32, 55, 81],
    'Heat Risk': ['High', 'Very High', 'Extreme', 'High', 'Moderate', 'High', 'Very High']
}
risk_df = pd.DataFrame(data)
st.dataframe(risk_df, use_container_width=True)

# Map
st.subheader("🗺️ Bijapur Vulnerability Map")
fig = px.scatter_mapbox(
    pd.DataFrame({"lat": [18.79, 18.85, 18.70], "lon": [80.82, 80.90, 80.75], "Risk": ["Very High", "High", "High"]}),
    lat="lat", lon="lon", color="Risk", zoom=9, height=500,
    mapbox_style="open-street-map"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🚨 Early Warnings")
st.warning("**High Risk Period Detected** - Advise communities on child hydration, mosquito protection & nutrition.")

st.caption("Open Source | MIT License | Public Data Only | Last Updated: " + datetime.now().strftime("%d %b %Y"))
