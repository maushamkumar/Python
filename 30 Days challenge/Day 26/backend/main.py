from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from weather_service import WeatherService
from email_service import EmailService
from datetime import datetime

app = FastAPI(title="WeatherBot Pro API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

weather_service = WeatherService()
email_service = EmailService()

class WeatherRequest(BaseModel):
    city: str
    user_id: Optional[str] = None
    email: Optional[str] = None

class UmbrellaResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    precipitation_chance: int
    need_umbrella: bool
    recommendation: str
    timestamp: str

@app.get("/")
async def root():
    return {"message": "WeatherBot Pro API is running! 🌦️"}

@app.post("/check-umbrella", response_model=UmbrellaResponse)
async def check_umbrella_need(request: WeatherRequest, background_tasks: BackgroundTasks):
    try:
        weather_data = weather_service.get_weather(request.city)
        
        # Logic to determine if umbrella is needed
        need_umbrella = determine_umbrella_need(weather_data)
        recommendation = get_recommendation(weather_data, need_umbrella)
        
        response = UmbrellaResponse(
            city=weather_data["city"],
            temperature=weather_data["temperature"],
            description=weather_data["description"],
            humidity=weather_data["humidity"],
            precipitation_chance=weather_data["precipitation_chance"],
            need_umbrella=need_umbrella,
            recommendation=recommendation,
            timestamp=datetime.now().isoformat()
        )
        
        # Background task for logging and email
        if request.user_id:
            background_tasks.add_task(log_weather_check, request.user_id, response)
        
        if request.email:
            background_tasks.add_task(send_email_notification, request.email, response)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/send-email-reminder")
async def send_email_reminder(request: WeatherRequest, background_tasks: BackgroundTasks):
    """Send email reminder for a specific city"""
    if not request.email:
        raise HTTPException(status_code=400, detail="Email address is required")
    
    try:
        weather_data = weather_service.get_weather(request.city)
        need_umbrella = determine_umbrella_need(weather_data)
        recommendation = get_recommendation(weather_data, need_umbrella)
        
        response = UmbrellaResponse(
            city=weather_data["city"],
            temperature=weather_data["temperature"],
            description=weather_data["description"],
            humidity=weather_data["humidity"],
            precipitation_chance=weather_data["precipitation_chance"],
            need_umbrella=need_umbrella,
            recommendation=recommendation,
            timestamp=datetime.now().isoformat()
        )
        
        # Send email in background
        background_tasks.add_task(send_email_notification, request.email, response)
        
        return {"message": f"Email reminder will be sent to {request.email}", "weather_data": response}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/weather/{city}")
async def get_weather_info(city: str):
    try:
        weather_data = weather_service.get_weather(city)
        return weather_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def determine_umbrella_need(weather_data: dict) -> bool:
    """Determine if user needs an umbrella based on weather conditions"""
    conditions = weather_data["description"].lower()
    precipitation_chance = weather_data["precipitation_chance"]
    
    # Umbrella needed if:
    # - Rain/drizzle/thunderstorm in description
    # - Precipitation chance > 30%
    rain_keywords = ["rain", "drizzle", "thunderstorm", "shower", "storm"]
    has_rain_keyword = any(keyword in conditions for keyword in rain_keywords)
    
    return has_rain_keyword or precipitation_chance > 30

def get_recommendation(weather_data: dict, need_umbrella: bool) -> str:
    """Get personalized recommendation"""
    temp = weather_data["temperature"]
    desc = weather_data["description"]
    
    if need_umbrella:
        if temp < 10:
            return f"🌧️❄️ Take an umbrella! It's {desc} and cold ({temp}°C). Stay warm and dry!"
        elif temp > 25:
            return f"🌧️☀️ Take an umbrella! It's {desc} and warm ({temp}°C). Perfect for staying cool and dry!"
        else:
            return f"🌧️ Take an umbrella! It's {desc} ({temp}°C). Better safe than sorry!"
    else:
        return f"☀️ No umbrella needed! It's {desc} ({temp}°C). Enjoy the nice weather!"

async def log_weather_check(user_id: str, response: UmbrellaResponse):
    """Background task to log weather checks"""
    print(f"Logged weather check for user {user_id}: {response.city} - Umbrella: {response.need_umbrella}")

async def send_email_notification(email: str, weather_data: UmbrellaResponse):
    """Background task to send email notification"""
    try:
        success = email_service.send_umbrella_reminder(email, weather_data.dict())
        if success:
            print(f"Email sent successfully to {email}")
        else:
            print(f"Failed to send email to {email}")
    except Exception as e:
        print(f"Error sending email to {email}: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)