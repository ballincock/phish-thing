from app.models.user import db
from datetime import datetime

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column(db.String(255), default='Unknown', nullable=False)
    trip_success = db.Column(db.Integer, default=0)
    primary_species = db.Column(db.String(100), default='None')
    lures_used = db.Column(db.String(255), default='None')
    time_elapsed = db.Column(db.String(50), default='0')
    season = db.Column(db.String(100), default='Unknown')
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
