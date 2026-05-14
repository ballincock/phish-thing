from app.models.user import db
from datetime import datetime

class WeatherLog(db.Model):
    __tablename__ = 'weather_logs'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_date = db.Column(db.String(50), nullable=False)
    pressure_low = db.Column(db.Float, default=1013.0)
    pressure_high = db.Column(db.Float, default=1013.0)
    wind_speed_low = db.Column(db.Float, default=0.0)
    wind_high = db.Column(db.Float, default=0.0)
    wind_dir = db.Column(db.String(10), default='N')
    temp_min = db.Column(db.Integer, default=0)
    temp_max = db.Column(db.Integer, default=0)
    trend_analysis = db.Column(db.String(255))
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
