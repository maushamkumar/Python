# WeatherBot Pro 🌦️☔

A smart umbrella reminder app that tells you whether you need to carry an umbrella based on real-time weather data.

## Features

- 🌡️ Real-time weather data fetching
- ☔ Smart umbrella recommendation logic
- 🎨 Beautiful Streamlit UI
- 🚀 FastAPI backend with automatic docs
- 📧 Email notifications (optional)
- 📊 Google Sheets logging (optional)
- 🔄 Background task processing

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Weather API**: OpenWeatherMap
- **Notifications**: Email (SMTP) 

## Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd 30\ Days\ challenge/
cd Day\ 26/
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 4. Run the Frontend

```bash
cd frontend
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Configuration

### Weather API (Optional)

1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
2. Set environment variable:
   ```bash
   export WEATHER_API_KEY="your_api_key_here"
   ```

### Email Notifications (Optional)

Set environment variables:
```bash
export EMAIL_ADDRESS="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
```

## API Endpoints

- `POST /check-umbrella` - Get umbrella recommendation
- `GET /weather/{city}` - Get weather data for a city

## Usage Examples

### API Call
```python
import requests

response = requests.post(
    "http://localhost:8000/check-umbrella",
    json={"city": "New York", "user_id": "user123"}
)
print(response.json())
```

### Response
```json
{
  "city": "New York",
  "temperature": 22.5,
  "description": "light rain",
  "humidity": 78,
  "precipitation_chance": 65,
  "need_umbrella": true,
  "recommendation": "🌧️ Take an umbrella! It's light rain (22.5°C). Better safe than sorry!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Development

### Project Structure
```
weatherbot_pro/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── weather_service.py   # Weather API integration
    ├── email_service.py     # Email service
├── frontend/
│   ├── app.py              # Streamlit app
├──requirements.txt
└── README.md
```

### Adding New Features

1. **New Weather Sources**: Extend `WeatherService` class
2. **Custom Logic**: Modify `determine_umbrella_need()` function
3. **UI Components**: Add new Streamlit components in `app.py`
4. **Notifications**: Extend notification services

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - feel free to use this project for learning and development!

## Troubleshooting

### Common Issues

1. **API Connection Error**: Make sure the FastAPI backend is running
2. **Weather Data Issues**: Check if you have a valid API key set
3. **Email Not Sending**: Verify SMTP settings and app passwords
4. **Sheets Not Logging**: Check Google Cloud credentials and permissions

### Support

For issues and questions, please create an issue in the repository.

---

Happy coding! 🚀 Don't forget your umbrella! ☔
```

## Running Instructions

1. **Start the Backend:**
   ```bash
   pip install -r requirements.txt
   cd backend
   uvicorn main:app --reload
   ```

2. **Start the Frontend:**
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. **Access the Application:**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Frontend: http://localhost:8501

The app works with mock data by default, but you can get a free API key from OpenWeatherMap for real weather data!