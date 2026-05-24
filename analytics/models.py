"""
From the necessities of the dashboard and session dashboard necessities, use this file to do so.
Other variables and table that are likely to need to be constructed are stuff like:
    > user favorite activities based on page visit duration
    > use data from within those pages (where they placed spot pins, etc), to make even more detailed and advanced recommendations to user in question.
"""

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

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_key = db.Column(db.String(100), unique=True, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(255))
    page_views = db.Column(db.Integer, default=1)
    duration_seconds = db.Column(db.Integer, default=0) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', foreign_keys=[user_id])
