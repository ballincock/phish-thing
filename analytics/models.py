from app.models.user import db  
from datetime import datetime

class UserVisit(db.Model):
    __tablename__ = 'user_visits'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) 
    endpoint = db.Column(db.String(150), nullable=False)                     
    ip_address = db.Column(db.String(45))                                   
    user_agent = db.Column(db.String(255))                                  
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id])
