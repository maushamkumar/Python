import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Dict
from dotenv import load_dotenv
load_dotenv()


class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email = os.getenv("EMAIL_ADDRESS")
        self.password = os.getenv("EMAIL_PASSWORD")
        
        # Check if email credentials are provided
        if not self.email or not self.password:
            print("⚠️  Email credentials not found. Set EMAIL_ADDRESS and EMAIL_PASSWORD environment variables.")
            print("📧 Email notifications will be simulated in console.")
    
    def send_umbrella_reminder(self, recipient: str, weather_data: Dict) -> bool:
        """Send umbrella reminder via email"""
        
        # If no credentials, simulate email sending
        if not self.email or not self.password:
            return self._simulate_email_send(recipient, weather_data)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = recipient
            msg['Subject'] = f"WeatherBot Pro: {'☔ Umbrella Needed!' if weather_data['need_umbrella'] else '☀️ No Umbrella Needed'} - {weather_data['city']}"
            
            # Create email body
            umbrella_status = "TAKE AN UMBRELLA! ☔" if weather_data['need_umbrella'] else "NO UMBRELLA NEEDED! ☀️"
            
            body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: {'#ff6b6b' if weather_data['need_umbrella'] else '#4ecdc4'}; color: white; padding: 20px; border-radius: 10px; text-align: center; }}
        .weather-info {{ background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin: 20px 0; }}
        .footer {{ color: #666; font-size: 12px; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{umbrella_status}</h1>
        <h2>{weather_data['city']}</h2>
    </div>
    
    <div class="weather-info">
        <h3>🌤️ Weather Details</h3>
        <ul>
            <li><strong>🌡️ Temperature:</strong> {weather_data['temperature']}°C</li>
            <li><strong>☁️ Conditions:</strong> {weather_data['description'].title()}</li>
            <li><strong>💧 Humidity:</strong> {weather_data['humidity']}%</li>
            <li><strong>🌧️ Rain Chance:</strong> {weather_data['precipitation_chance']}%</li>
        </ul>
        
        <p><strong>💡 Recommendation:</strong> {weather_data['recommendation']}</p>
    </div>
    
    <p>Have a great day!</p>
    
    <div class="footer">
        <p>This email was sent by WeatherBot Pro 🤖<br>
        Generated at: {weather_data['timestamp']}</p>
    </div>
</body>
</html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, recipient, text)
            server.quit()
            
            print(f"✅ Email sent successfully to {recipient}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {recipient}: {str(e)}")
            return False
    
    def _simulate_email_send(self, recipient: str, weather_data: Dict) -> bool:
        """Simulate email sending when credentials are not available"""
        umbrella_status = "TAKE AN UMBRELLA! ☔" if weather_data['need_umbrella'] else "NO UMBRELLA NEEDED! ☀️"
        
        print(f"\n{'='*60}")
        print(f"📧 SIMULATED EMAIL TO: {recipient}")
        print(f"{'='*60}")
        print(f"Subject: WeatherBot Pro: {umbrella_status} - {weather_data['city']}")
        print(f"\n{umbrella_status}")
        print(f"Location: {weather_data['city']}")
        print(f"Temperature: {weather_data['temperature']}°C")
        print(f"Conditions: {weather_data['description'].title()}")
        print(f"Humidity: {weather_data['humidity']}%")
        print(f"Rain Chance: {weather_data['precipitation_chance']}%")
        print(f"\nRecommendation: {weather_data['recommendation']}")
        print(f"Timestamp: {weather_data['timestamp']}")
        print(f"{'='*60}\n")
        
        return True