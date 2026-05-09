from flask import Flask
from flask_talisman import Talisman
from config import Config
from app.models.user import db
from app.blueprints.auth import auth_bp
from app.blueprints.dashboard import dash_bp
from app.blueprints.gallery import gallery_bp
from app.blueprints.user import user_bp
from app.blueprints.security import security_bp

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(Config)

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

    with app.app_context():
        db.create_all()

    return app
