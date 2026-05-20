from app.models.user.user import db
from datetime import datetime

class Catch(db.Model):
    __tablename__ = 'catches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    species = db.Column(db.String(100), nullable=False)
    time_caught = db.Column(db.String(50))   
    date_caught = db.Column(db.String(50))   
    weather_conditions = db.Column(db.String(255))
    lure_used = db.Column(db.String(255))
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
