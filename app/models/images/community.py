from app.models.user import db
from datetime import datetime

class PublicCatch(db.Model):
    __tablename__ = 'public_catches'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    author = db.relationship('User', backref=db.backref('public_catches', lazy=True))
    image_path = db.Column(db.String(255), nullable=False)
    
    species = db.Column(db.String(100))
    lure_used = db.Column(db.String(100))
    time_of_day = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    pressure = db.Column(db.Float)
    cloud_cover = db.Column(db.String(50))
    moon_cycle = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship('User', backref='public_posts')
    comments = db.relationship('Comment', backref='post', cascade="all, delete-orphan", lazy='dynamic')

    def to_dict(self):
        return {
            "id": self.id,
            "image_path": self.image_path,
            "species": self.species,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "notes": self.notes,
            "temp": self.temp,
            "moon_phase": self.moon_phase,
            "author_name": self.author.username,
            "author_pfp": self.author.profile_picture
        }

class LikeRecord(db.Model):
    __tablename__ = 'like_records'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('public_catches.id'))
    status = db.Column(db.Integer) 

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('public_catches.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id')) 
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    user = db.relationship('User')

class Friendship(db.Model):
    __tablename__ = 'friendships'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))     
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))   
    status = db.Column(db.String(20), default='pending')           
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[user_id], backref='sent_requests')
    receiver = db.relationship('User', foreign_keys=[friend_id], backref='received_requests')
