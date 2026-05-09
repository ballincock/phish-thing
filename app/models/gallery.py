from app.models.user import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os

class GalleryImage(db.Model):
    __tablename__ = 'gallery_images'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Metadata Fields
    species = db.Column(db.String(100))
    lure_used = db.Column(db.String(100))
    season = db.Column(db.String(50))
    time_of_day = db.Column(db.String(50))
    pressure = db.Column(db.Float)
    temperature = db.Column(db.Float)
    cloud_cover = db.Column(db.String(50))
    moon_cycle = db.Column(db.String(50))
    notes = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('gallery_items', lazy=True))
