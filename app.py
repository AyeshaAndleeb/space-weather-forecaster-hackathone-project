import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import datetime

# -------------------------------
# 🚀 Streamlit App - Space Weather Dashboard
# -------------------------------

# Set page title & icon
st.set_page_config(page_title="Space Weather AI 🌌", page_icon="🚀", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
        body {
            background-color: #0E1117;
            color: white;
        }
        .stApp {
            background-color: #1E1E1E;
        }
        .title {
            text-align: center;
            font-size: 35px;
            font-weight: bold;
            color: #00C3FF;
        }
        .sub-title {
            text-align: center;
            font-size: 20px;
            color: #F4A261;
        }
        .big-text {
            font-size: 18px;
            color: #E9C46A;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="title">🚀 AI-Powered Space Weather Forecaster 🌌</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">🔭 Stay Updated with Real-Time Space Weather Predictions</p>', unsafe_allow_html=True)

# API URL - NASA Space Weather Prediction
API_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

# Fetch data function
@st.cache_data
def fetch_space_weather():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

# Fetch the data
data = fetch_space_weather()

# -------------------------------
# 🌟 Displaying Space Weather Data
# -------------------------------

if data:
    st.subheader("📊 Real-Time Space Weather Data")

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Convert timestamp to readable format
    df["time_tag"] = pd.to_datetime(df["time_tag"])

    # Display last 5 readings
    st.dataframe(df.tail(), use_container_width=True)

    # -------------------------------
    # 🌞 Solar Activity Trends
    # -------------------------------

    st.subheader("☀️ Solar Activity Over Time")
    fig = px.line(df, x="time_tag", y="kp_index", markers=True, title="Solar Geomagnetic Activity")
    fig.update_traces(line_color="#FF5733")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 🚨 AI-Based Forecasting
    # -------------------------------

    latest_kp_index = df["kp_index"].iloc[-1]

    st.subheader("🔮 AI-Based Space Weather Forecast")
    if latest_kp_index > 5:
        st.error(f"⚠️ High geomagnetic activity detected! (Kp Index: {latest_kp_index})")
        st.write("🚀 Potential space weather storms detected. Astronauts and satellites may be affected!")
    else:
        st.success(f"✅ Space weather is stable (Kp Index: {latest_kp_index})")
        st.write("🛰️ No major geomagnetic disturbances expected.")

else:
    st.warning("⚠️ Unable to fetch space weather data. Please try again later.")

# -------------------------------
# 🌍 Footer
# -------------------------------
st.markdown("---")
st.write("📡 Data Source: NASA | Developed by Ayesha Andleeb🚀")