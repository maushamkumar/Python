import requests
import os
from typing import Dict

class WeatherService:
    def __init__(self):
        # Using OpenWeatherMap API (free tier)
        # Get your API key from: https://openweathermap.org/api
        self.api_key = os.getenv("WEATHER_API_KEY", "demo_key")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str) -> Dict:
        """Fetch weather data from OpenWeatherMap API"""
        
        # For demo purposes, return mock data if no API key
        if self.api_key == "demo_key":
            return self._get_mock_weather(city)
        
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "precipitation_chance": self._calculate_precipitation_chance(data),
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"]
            }
            
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch weather data: {str(e)}")
    
    def _calculate_precipitation_chance(self, data: Dict) -> int:
        """Calculate precipitation chance based on weather conditions"""
        # Simplified calculation based on humidity and weather conditions
        humidity = data["main"]["humidity"]
        weather_main = data["weather"][0]["main"].lower()
        
        if weather_main in ["rain", "thunderstorm", "drizzle"]:
            return min(80 + humidity // 5, 100)
        elif weather_main in ["clouds"]:
            return min(humidity // 2, 60)
        else:
            return max(humidity // 4, 5)
    
    def _get_mock_weather(self, city: str) -> Dict:
        """Return mock weather data for demo purposes"""
        import random
        
        mock_conditions = [
            ("sunny", 25, 45, 10),
            ("cloudy", 20, 65, 25),
            ("light rain", 18, 85, 70),
            ("thunderstorm", 22, 90, 85),
            ("partly cloudy", 23, 55, 20)
        ]
        
        condition, temp, humidity, precip = random.choice(mock_conditions)
        
        return {
            "city": city.title(),
            "temperature": temp + random.randint(-5, 5),
            "description": condition,
            "humidity": humidity + random.randint(-10, 10),
            "precipitation_chance": precip + random.randint(-15, 15),
            "pressure": 1013 + random.randint(-20, 20),
            "wind_speed": random.randint(2, 15)
        }