from app.models.user import db
from datetime import datetime

class ApiWeatherLog(db.Model):
    __tablename__ = 'api_weather_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location = db.Column(db.String(255), nullable=False)
    temp = db.Column(db.Float, default=0.0)
    pressure = db.Column(db.Float, default=1013.0)
    precip = db.Column(db.Float, default=0.0)        
    wind_speed = db.Column(db.Float, default=0.0)
    wind_dir = db.Column(db.String(10))
    trends = db.Column(db.String(255))               
    reasons = db.Column(db.Text)               
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
