from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    security_question = db.Column(db.String(255), nullable=False)
    security_answer_hash = db.Column(db.String(256), nullable=False)
    backup_email = db.Column(db.String(120))
    mnemonic = db.Column(db.String(255), nullable=False)

    # NEW COLUMNS
    display_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    profile_picture = db.Column(db.String(255), default='uploads/profiles/default.png')
    reddit = db.Column(db.String(100))
    twitter = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    youtube = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    favorite_species = db.Column(db.String(100))
    favorite_pb = db.Column(db.String(100))
    fishing_region = db.Column(db.String(100))

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
