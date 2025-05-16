from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from app.config import Config
from threading import Thread

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)



    with app.app_context():
        db.create_all()

    @app.before_first_request
    def start_mqtt_client():
        from app.services.mqtt_service import start_mqtt_client
        start_mqtt_client(app)

    return app