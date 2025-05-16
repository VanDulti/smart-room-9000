# app/routes/main.py
from flask import Blueprint, render_template, jsonify, request
from app.models.sensors import SensorData
from sqlalchemy import desc
from datetime import datetime, timedelta
import time

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Render the main page"""
    # Get latest sensor readings
    latest_readings = {}

    # MQTT Topics
    topics = [
        "/smartroom9000/mmwave",
        "/smartroom9000/ambientlight",
        "/smartroom9000/humidity",
        "/smartroom9000/temperature",
        "/smartroom9000/ventilation",
        "/smartroom9000/heating",
        "/smartroom9000/lightcontrol"
    ]

    for topic in topics:
        data = SensorData.query.filter_by(topic=topic).order_by(desc(SensorData.timestamp)).first()
        if data:
            # Extract readable name from topic
            sensor_name = topic.split('/')[-1]
            latest_readings[sensor_name] = {
                'value': data.value,
                'timestamp': data.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }

    # Pass current time to template
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template('index.html', readings=latest_readings, current_time=current_time)


@main_bp.route('/api/data')
def get_data():
    """API endpoint to get sensor data"""
    topic = request.args.get('topic')
    hours = request.args.get('hours', 24, type=int)

    # Set time limit
    time_limit = datetime.utcnow() - timedelta(hours=hours)

    # Query data
    query = SensorData.query.filter(SensorData.timestamp >= time_limit)

    if topic:
        query = query.filter(SensorData.topic == topic)

    data = query.order_by(desc(SensorData.timestamp)).all()

    return jsonify([item.to_dict() for item in data])