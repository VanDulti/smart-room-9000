from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from webservice.app.config import Config
from threading import Thread
from app.services import mqtt_service
from webservice.app.services.mqtt_service import start_mqtt_service

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    start_mqtt_service()

    from app.routes import main_bp
    app.register_blueprint(main_bp)



    with app.app_context():
        db.create_all()

    return app