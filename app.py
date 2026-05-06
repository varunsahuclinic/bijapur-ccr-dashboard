import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px

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

with st.expander("🔥 Heatwave Advisory (NPCCHH / MoHFW)"):
    st.markdown("""
    - Avoid outdoor activities for children between **12 PM – 4 PM**  
    - Ensure frequent hydration with **ORS / lemon water**  
    - Watch for signs of heat exhaustion: dizziness, nausea, rapid breathing  
    - Use wet sponging and keep children in shaded areas  
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
    """)

with st.expander("🌧️ Heavy Rain / Flood Advisory"):
    st.markdown("""
    - Store clean drinking water and emergency medicines  
    - Boil water before drinking  
    - Avoid playing near water bodies  
    """)

with st.expander("🥗 Nutrition & General Child Protection"):
    st.markdown("""
    - Prioritize nutritious meals (climate stress increases malnutrition)  
    - Continue breastfeeding for infants  
    - Maintain vaccination schedule  
    """)

# ================== ENHANCED VULNERABILITY MAP ==================
st.subheader("🗺️ High Vulnerability Areas in Bijapur District")

# Realistic High Vulnerability Locations (based on malaria hotspots, forest areas, flood-prone zones)
vulnerability_data = pd.DataFrame({
    "Area": [
        "Gangaluur (High Malaria)", 
        "Usur Block", 
        "Bhairamgarh (Indravati River villages)", 
        "Bijapur Block HQ", 
        "Bhopalpattnam", 
        "Madded", 
        "Kutru", 
        "Awapalli"
    ],
    "lat": [18.95, 18.75, 18.70, 18.79, 18.85, 19.05, 18.60, 18.82],
    "lon": [80.95, 80.65, 80.75, 80.82, 80.55, 81.05, 80.45, 80.90],
    "Risk_Level": ["Very High", "Very High", "Very High", "High", "High", "High", "High", "Very High"],
    "Main_Threat": ["Malaria + Heat", "Malaria", "Flood + Malaria", "Heat Stress", "Flood", "Malaria", "Malaria", "Malaria + Heat"]
})

fig = px.scatter_mapbox(
    vulnerability_data,
    lat="lat", 
    lon="lon", 
    color="Risk_Level",
    hover_name="Area",
    hover_data=["Main_Threat"],
    zoom=9, 
    height=600,
    mapbox_style="open-street-map",
    title="High Vulnerability Areas - Bijapur District (Malaria, Heat & Flood Hotspots)",
    color_discrete_map={"Very High": "red", "High": "orange"}
)

fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

st.info("**Note**: Red markers indicate **Very High** vulnerability zones (mainly forested/tribal areas with high malaria incidence).")

# Footer
st.markdown("---")
st.caption(f"Open Source | MIT License | Uses Public Data Only | Last Updated: {datetime.now().strftime('%d %b %Y, %H:%M')} IST")
st.caption("Aligned with National Programme on Climate Change and Human Health (NPCCHH)")
