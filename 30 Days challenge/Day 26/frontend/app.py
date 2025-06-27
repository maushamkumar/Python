import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="WeatherBot Pro",
    page_icon="☔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .umbrella-needed {
        background-color: #ff6b6b;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
    }
    .no-umbrella {
        background-color: #4ecdc4;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
    }
    .weather-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("🌦️ WeatherBot Pro")
    st.subheader("Your Smart Umbrella Reminder Assistant")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        user_id = st.text_input("User ID (Optional)", placeholder="your_user_id")
        
        st.header("📍 Locations")
        favorite_cities = st.multiselect(
            "Favorite Cities",
            ["New York", "London", "Tokyo", "Paris", "Mumbai", "Sydney"],
            default=["New York", "London"]
        )
        
        st.header("🔔 Email Notifications")
        user_email = st.text_input("Email Address (Optional)", placeholder="your@email.com")
        enable_notifications = st.checkbox("Enable Email Notifications", value=True)
        notification_time = st.time_input("Daily Reminder Time", value=datetime.now().time())
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🌍 Check Weather")
        
        # City input
        city = st.text_input("Enter City Name", placeholder="e.g., New York, London, Tokyo")
        
        # Quick city buttons
        st.write("Quick Select:")
        col_quick1, col_quick2, col_quick3, col_quick4 = st.columns(4)
        
        with col_quick1:
            if st.button("🗽 New York"):
                city = "New York"
        with col_quick2:
            if st.button("🌉 London"):
                city = "London"
        with col_quick3:
            if st.button("🗼 Tokyo"):
                city = "Tokyo"
        with col_quick4:
            if st.button("🕌 Mumbai"):
                city = "Mumbai"
        
        # Check weather button
        if st.button("🔍 Check Weather & Umbrella Need", type="primary"):
            if city:
                check_weather(city, user_id, user_email)
            else:
                st.error("Please enter a city name!")
    
    with col2:
        st.header("📊 Quick Stats")
        
        # Display favorite cities weather
        if favorite_cities:
            st.subheader("Favorite Cities")
            for fav_city in favorite_cities:
                with st.expander(f"🏙️ {fav_city}"):
                    get_quick_weather(fav_city)

def check_weather(city: str, user_id: str = None, user_email: str = None):
    """Check weather and umbrella recommendation"""
    try:
        with st.spinner(f"Checking weather for {city}..."):
            # Prepare request data
            request_data = {"city": city}
            if user_id:
                request_data["user_id"] = user_id
            if user_email:
                request_data["email"] = user_email
            
            # Make API call
            response = requests.post(
                f"{API_BASE_URL}/check-umbrella",
                json=request_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                display_weather_result(data)
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                
    except requests.ConnectionError:
        st.error("❌ Cannot connect to WeatherBot API. Make sure the backend is running!")
        st.info("💡 To start the backend, run: `uvicorn main:app --reload` in the backend directory")
    except requests.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

def display_weather_result(data: dict):
    """Display weather results in a nice format"""
    
    # Main recommendation
    if data["need_umbrella"]:
        st.markdown(f"""
        <div class="umbrella-needed">
            ☔ TAKE AN UMBRELLA! ☔<br>
            {data["recommendation"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="no-umbrella">
            ☀️ NO UMBRELLA NEEDED! ☀️<br>
            {data["recommendation"]}
        </div>
        """, unsafe_allow_html=True)
    
    # Weather details
    st.markdown("---")
    st.subheader(f"🌤️ Weather Details for {data['city']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🌡️ Temperature",
            value=f"{data['temperature']}°C"
        )
    
    with col2:
        st.metric(
            label="💧 Humidity",
            value=f"{data['humidity']}%"
        )
    
    with col3:
        st.metric(
            label="🌧️ Rain Chance",
            value=f"{data['precipitation_chance']}%"
        )
    
    with col4:
        st.metric(
            label="☁️ Conditions",
            value=data['description'].title()
        )
    
    # Timestamp
    st.caption(f"Last updated: {data['timestamp']}")
    
    # Additional actions
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh"):
            st.rerun()
    
    with col2:
        email_input = st.text_input("Email for reminder:", key="email_input")
        if st.button("📧 Send Email Reminder"):
            if email_input:
                send_email_reminder(data, email_input)
            else:
                st.error("Please enter an email address!")
    
    with col3:
        if st.button("📱 Get Daily Reminders"):
            st.info("💡 Enter your email in the sidebar and check weather to enable daily reminders!")

def get_quick_weather(city: str):
    """Get quick weather info for sidebar"""
    try:
        response = requests.get(f"{API_BASE_URL}/weather/{city}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            st.write(f"🌡️ {data['temperature']}°C")
            st.write(f"☁️ {data['description'].title()}")
            st.write(f"💧 {data['humidity']}% humidity")
        else:
            st.write("❌ Unable to fetch")
    except:
        st.write("❌ Connection error")

def send_email_reminder(data: dict, email: str):
    """Send email reminder"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/send-email-reminder",
            json={"city": data["city"], "email": email},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            st.success(f"✅ {result['message']}")
            
            # Show preview of what will be sent
            with st.expander("📧 Email Preview"):
                st.write(f"**To:** {email}")
                st.write(f"**Subject:** WeatherBot Pro: {'☔ Umbrella Needed!' if data['need_umbrella'] else '☀️ No Umbrella Needed'} - {data['city']}")
                st.write(f"**Content:** {data['recommendation']}")
        else:
            st.error(f"❌ Failed to send email: {response.json().get('detail', 'Unknown error')}")
            
    except requests.ConnectionError:
        st.error("❌ Cannot connect to WeatherBot API for email sending!")
    except Exception as e:
        st.error(f"❌ Error sending email: {str(e)}")

def save_to_sheets(data: dict):
    """Save to Google Sheets (placeholder)"""
    st.info("📊 Google Sheets integration would be implemented here!")
    st.json({
        "action": "save_to_sheets",
        "spreadsheet_id": "your_sheet_id",
        "data": data
    })

# Run the app
if __name__ == "__main__":
    main()