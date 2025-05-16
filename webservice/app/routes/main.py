# app/routes/main.py
from flask import Blueprint, render_template, jsonify, request
from webservice.app.models.sensors import SensorData
from sqlalchemy import desc
from datetime import datetime, timedelta
import time

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    latest_readings = {}

    for topic in services.mqtt_service.MQTT_TOPICS:
        data = SensorData.query.filter_by(topic=topic).order_by(desc(SensorData.timestamp)).first()
        if data:
            sensor_name = topic.split('/')[-1]
            latest_readings[sensor_name] = {
                'value': data.value,
                'timestamp': data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }

    # Pass current time to template
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('index.html', readings=latest_readings, current_time=current_time)


