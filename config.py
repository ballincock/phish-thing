import os

class Config:
    DEBUG = True
    
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fh209dj12h0912djxhg03fdjhg84')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///pys.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    ### MAIL_SERVER = os.environ.get('MAIL_SERVER', '://gmail.com')
    #MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'on', '1']
    #MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    #MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    #MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@yourdomain.com')
    ###
    
