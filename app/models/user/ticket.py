from app.models.user.user import db  
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'tickets'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Open')  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    client = db.relationship('User', foreign_keys=[client_id])
    messages = db.relationship('TicketMessage', backref='ticket', lazy=True, cascade="all, delete-orphan")

class TicketMessage(db.Model):
    __tablename__ = 'ticket_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.String(1000), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id])
