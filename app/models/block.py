from app.models.user import db
from datetime import datetime

class BlockList(db.Model):
    __tablename__ = 'blocklists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    blocker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blocked_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
