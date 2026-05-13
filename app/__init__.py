from flask import Flask
from flask_talisman import Talisman
from config import Config
from app.models.user import db
from app.blueprints.auth import auth_bp
from app.blueprints.dashboard import dash_bp
from app.blueprints.gallery import gallery_bp
from app.blueprints.user import user_bp
from app.blueprints.security import security_bp
from app.blueprints.community import community_bp
from app.blueprints.gallery_profile import gallery_profile_bp
from app.blueprints.calcs import fishing_bp
from app.blueprints.current_weather import weather_bp
from app.blueprints.historical_weather import historical_bp

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    db.init_app(app)

    csp = {
        'default-src': "'self'",
        'script-src': [
            "'self'", 
            "https://pyscript.net", 
            "'unsafe-inline'", 
            "'unsafe-eval'"
        ],
        'style-src': [
            "'self'", 
            "https://pyscript.net", 
            "'unsafe-inline'"
        ],
        'connect-src': [
            "'self'", 
            "https://pyscript.net"
        ],
        'img-src': [
            "'self'", 
            "data:", 
            "blob:", 
            "http://localhost" 
        ],
        'worker-src': ["'self'", "blob:"] 
    }

    Talisman(app, content_security_policy=csp)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dash_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(community_bp)
    app.register_blueprint(gallery_profile_bp)
    app.register_blueprint(fishing_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(historical_bp)

    with app.app_context():
        from app.models.weather_log import ApiWeatherLog
        db.create_all()

    return app
