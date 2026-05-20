from flask import Flask
from flask_talisman import Talisman
from config import Config
from app.models.user import db
from app.blueprints.session.auth import auth_bp
from app.blueprints.session.dashboard import dash_bp
from app.blueprints.images.gallery import gallery_bp
from app.blueprints.user.user import user_bp
from app.blueprints.user.security import security_bp
from app.blueprints.images.community import community_bp
from app.blueprints.user.gallery_profile import gallery_profile_bp
from app.blueprints.calculators.calcs import fishing_bp
from app.blueprints.weather.current_weather import weather_bp
from app.blueprints.weather.historical_weather import historical_bp
from app.blueprints.weather.weather_predictions import predictions_bp
from app.blueprints.user.messages import messages_bp
from app.blueprints.maps.map_log import map_log_bp
from app.blueprints.maps.community_map import community_map_bp
from app.blueprints.calculators.hydrology_calcs import hydrology_bp
from app.blueprints.support import support
from app.blueprints.user.tickets import tickets_bp

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
    app.register_blueprint(hydrology_bp)
    app.register_blueprint(support)
    app.register_blueprint(tickets_bp)

    with app.app_context():
        from app.models.weather.weather_log import ApiWeatherLog
        from app.models.trips.catch import Catch
        from app.models.trips.trip import Trip
        from app.models.weather.weather_log_summary import WeatherLog
        from app.models.messages.message import Message
        from app.models.messages.block import BlockList
        from app.models.map.spot_pin import SpotPin
        from app.models.map.community_pin import CommunityPin
        db.create_all()

    return app
