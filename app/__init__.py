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
from app.blueprints.weather_predictions import predictions_bp
from app.blueprints.messages import messages_bp
from app.blueprints.map_log import map_log_bp
from app.blueprints.community_map import community_map_bp


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
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.js",
            "'unsafe-inline'",
            "'unsafe-eval'"
        ],
        'style-src': [
            "'self'",
            "https://pyscript.net",
            "https://unpkg.com/leaflet@1.9.4/dist/leaflet.css", 
            "'unsafe-inline'"
        ],
        'connect-src': [
            "'self'",
            "https://pyscript.net",
            "https://*.tile.openstreetmap.org",
            "://visualcrossing.com",
            "visualcrossing.com",
            "http://localhost:5000",
            "http://127.0.0.1:5000"
        ],
        'img-src': [
            "'self'",
            "data:",
            "blob:",
            "https://*.tile.openstreetmap.org",
            "http://localhost:5000",
            "http://127.0.0.1:5000",
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
    app.register_blueprint(predictions_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(map_log_bp)
    app.register_blueprint(community_map_bp)

    with app.app_context():
        from app.models.weather_log import ApiWeatherLog
        from app.models.catch import Catch
        from app.models.trip import Trip
        from app.models.weather_log_summary import WeatherLog
        from app.models.message import Message
        from app.models.block import BlockList
        from app.models.spot_pin import SpotPin
        from app.models.community_pin import CommunityPin
        db.create_all()

    return app
