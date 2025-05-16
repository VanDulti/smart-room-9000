import threading
from datetime import datetime

from app.config import Config
from app.smartroom_mqtt import start_mqtt_client
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    start_mqtt_service(app)

    from app.routes import main_bp
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app

def start_mqtt_service(app):
    def actual():
        start_mqtt_client(host='pi4felix.local',
                          port=1883,
                          on_data=lambda timestamp, sensor, value: store_measurement(app, timestamp, sensor, value))

    thread = threading.Thread(target=actual)
    thread.daemon = True  # Ensures the thread exits when the program terminates
    thread.start()
    print("MQTT service started in a separate thread.")


def store_measurement(app, timestamp: datetime, sensor: str, value: float):
    print(f'storing in db: {timestamp} {sensor} {value}')
    sensor_data = SensorData(timestamp=timestamp, topic=sensor, value=value)
    with app.app_context():
        app.db.session.add(sensor_data)
        app.db.session.commit()
