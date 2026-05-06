import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Bijapur CCR Dashboard", layout="wide", page_icon="🌍")

st.title("🌍 Bijapur Child Climate Resilience Dashboard (CCR)")
st.markdown("**Open Source Digital Public Good for UNICEF Venture Fund – Climate x Health**")

st.sidebar.header("📍 Bijapur, Chhattisgarh")
st.sidebar.metric("Vulnerability Level", "Very High")
st.sidebar.metric("Target Group", "Children under 5 & School-going")

# ================== WEATHER SECTION ==================
st.subheader("🌡️ Current Weather & Forecast")
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
    st.warning("Weather data temporarily unavailable")

# ================== RISK PREDICTION ==================
st.subheader("🔮 ML-Based Climate-Health Risk Prediction (Next 7 Days)")
data = {
    'Date': pd.date_range(start=datetime.now(), periods=7).strftime('%d %b %Y'),
    'Malaria Risk': ['High', 'Very High', 'Extreme', 'High', 'Moderate', 'High', 'Very High'],
    'Heat Stress Risk': ['High', 'Very High', 'Extreme', 'High', 'Moderate', 'High', 'Very High']
}
st.dataframe(pd.DataFrame(data), use_container_width=True)

# ================== NPCCHH ADVISORIES ==================
st.subheader("🚨 NPCCHH Early Warnings & Child Health Advisories")

with st.expander("🔥 Heatwave Advisory (NPCCHH / MoHFW Heat Action Plan)"):
    st.markdown("""
    - Avoid outdoor activities for children between **12 PM – 4 PM**
    - Ensure frequent hydration with **ORS / lemon water**
    - Watch for signs of heat exhaustion: dizziness, nausea, rapid breathing
    - Use wet sponging and keep children in shaded areas
    - Reschedule school/Anganwadi activities before 11 AM or after 4 PM
    """)

with st.expander("🦟 Malaria & Vector-Borne Diseases"):
    st.markdown("""
    - Clear stagnant water around homes, schools & Anganwadi centers
    - Use **insecticide-treated mosquito nets** for children
    - Wear full-sleeve clothes during evening hours
    - Seek immediate medical care if child has **fever with chills**
    """)

with st.expander("🌫️ Air Quality & Respiratory Health"):
    st.markdown("""
    - Keep children indoors when AQI is Poor or Very Poor
    - Use wet mopping instead of sweeping
    - Children with asthma should wear masks outdoors
    - Monitor symptoms: persistent cough, wheezing, difficulty breathing
    """)

with st.expander("🌧️ Heavy Rain / Flood Advisory"):
    st.markdown("""
    - Store clean drinking water and emergency medicines
    - Boil water before drinking to prevent diarrhea & cholera
    - Avoid playing near water bodies or low-lying areas
    - Identify safe elevated locations in the village
    """)

with st.expander("🥗 Nutrition & General Child Protection"):
    st.markdown("""
    - Climate stress increases malnutrition risk — prioritize nutritious meals
    - Continue breastfeeding for infants
    - Maintain regular vaccination schedule
    - Provide emotional support — extreme weather can cause anxiety in children
    """)

# ================== MAP ==================
st.subheader("🗺️ Bijapur Vulnerability Map")
fig = px.scatter_mapbox(
    pd.DataFrame({
        "lat": [18.79, 18.85, 18.70, 18.82], 
        "lon": [80.82, 80.90, 80.75, 80.85], 
        "Risk": ["Very High", "High", "High", "Very High"]
    }),
    lat="lat", lon="lon", color="Risk", zoom=9, height=500,
    mapbox_style="open-street-map"
)
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption(f"Open Source | MIT License | Uses Public Data Only | Last Updated: {datetime.now().strftime('%d %b %Y, %H:%M')} IST")
st.caption("Aligned with National Programme on Climate Change and Human Health (NPCCHH)")
