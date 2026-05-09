import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fh209dj12h0912djxhg03fdjhg84')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pys.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
