# app/routes/main.py
from flask import Blueprint, render_template
from webservice.app.models.sensors import SensorData
from webservice.app.config import Config
# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    topics = list(Config.MQTT_TOPICS.values())

    sensor_data = {}

    for topic in topics:
        data = SensorData.query.filter_by(topic=topic).order_by(SensorData.timestamp.desc()).limit(100).all()
        sensor_data[topic] = [item.to_dict() for item in data]

    return render_template('index.html', sensor_data=sensor_data, topics=topics)
