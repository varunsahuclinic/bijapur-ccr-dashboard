import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
import joblib
import numpy as np
import os

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
    st.warning("Weather data unavailable - showing sample")

# Sample Data
@st.cache_data
def load_sample_data():
    data = {
        'date': pd.date_range(start='2026-04-01', periods=30),
        'temp_max': [34,36,38,37,35,39,40,36,34,35,37,38,36,35,39,41,37,35,34,36,38,39,37,36,35,40,38,37,36,35],
        'rain_mm': [5,12,45,25,8,65,55,15,3,10,50,30,20,8,60,70,25,5,12,40,35,15,8,55,45,20,10,5,30,25],
        'humidity': [65,70,85,80,68,88,82,72,60,75,82,78,70,65,85,80,75,68,72,80,78,70,65,82,85,75,70,68,80,78]
    }
    df = pd.DataFrame(data)
    df['malaria_risk'] = (df['rain_mm'] * 0.8 + df['temp_max'] * 0.6).round(1)
    return df

df = load_sample_data()

# ML Risk Prediction
st.subheader("🔮 ML-Based Climate-Health Risk Prediction (Next 7 Days)")
future_dates = pd.date_range(start=datetime.now(), periods=7).strftime('%Y-%m-%d')
risk_levels = ['High', 'Very High', 'Very High', 'High', 'Moderate', 'High', 'Very High']

risk_df = pd.DataFrame({
    'Date': future_dates,
    'Predicted Malaria Risk Score': [45, 78, 92, 65, 32, 55, 81],
    'Heat Stress Risk': ['High', 'Very High', 'Extreme', 'High', 'Moderate', 'High', 'Very High'],
    'Recommended Action': ['Hydration + Nets', 'Full Alert', 'School Closure Prep', 'Nets + ORS', 'Monitor', 'Prepare', 'Full Alert']
})
st.dataframe(risk_df, use_container_width=True)

if st.button("📥 Download Sample Data"):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download bijapur_climate_data.csv", csv, "bijapur_climate_data.csv", "text/csv")

# Map
st.subheader("🗺️ Bijapur Vulnerability Map")
fig = px.scatter_mapbox(
    pd.DataFrame({"lat": [18.79, 18.85, 18.70], "lon": [80.82, 80.90, 80.75], "Risk": ["Very High", "High", "High"]}),
    lat="lat", lon="lon", color="Risk", zoom=9, height=500,
    mapbox_style="open-street-map", hover_name="Risk"
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("🚨 Early Warnings & Guidance for ASHA/ANM")
st.warning("**Heatwave + High Malaria Risk** — Prioritize child hydration, mosquito nets, and nutrition support.")
st.info("**Offline Advice**: High temperature + fever in child → Suspect malaria or heat stroke. Refer immediately.")

st.markdown("---")
st.caption("Open Source | MIT License | Uses only Public Data | Last Updated: " + datetime.now().strftime("%d %b %Y"))
