from app.models.user.user import db
from datetime import datetime

class CommunityPin(db.Model):
    __tablename__ = 'community_pins'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    spot_name = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    species = db.Column(db.String(100))
    lure_used = db.Column(db.String(255))
    time_of_year = db.Column(db.String(100))
    pressure = db.Column(db.String(50))
    cloud_cover = db.Column(db.String(50))
    rain = db.Column(db.String(50))
    temp = db.Column(db.String(50))
    wind = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref=db.backref('community_pins', lazy=True))
