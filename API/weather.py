import streamlit as st
import requests

API_KEY = ""

def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    st.write("📦 Status:", response.status_code)
    st.write("📨 Raw response:", response.text)

    if response.status_code == 200:
        return response.json()
    else:
        return None

st.set_page_config(page_title="🌦️ Kulti Weather App", page_icon="🌤️")
st.title("🌤️ Live Weather App")
st.markdown("Get real-time weather info for **Kulti** or anywhere in West Bengal")

default_city = "Kulti, West Bengal, IN"
city = st.text_input("Enter city name:", value=default_city)

if st.button("Get Weather"):
    data = get_weather(city)
    if data:
        st.subheader(f"📍 Weather in {data['name']}, {data['sys']['country']}")
        st.write("**🌡️ Temperature:**", data["main"]["temp"], "°C")
        st.write("**☁️ Weather:**", data["weather"][0]["description"].title())
        st.write("**💧 Humidity:**", data["main"]["humidity"], "%")
        st.write("**🌬️ Wind Speed:**", data["wind"]["speed"], "m/s")
    else:
        st.error("❌ Could not fetch data. Try a more specific city name.")
