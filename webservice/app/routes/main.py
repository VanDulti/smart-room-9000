# app/routes/main.py
from flask import Blueprint, render_template, jsonify, request
from app.models.sensors import SensorData
from sqlalchemy import desc
from datetime import datetime, timedelta
from app.config import Config
import time
import logging
from app import db

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    logging.info("Index route accessed")
    latest_readings = {}
    sensor_data = {}
    # Using only the friendly names (topic_name) for queries
    for mqtt_topic, topic_name in Config.MQTT_TOPICS.items():
        logging.warning(f"Processing topic: {mqtt_topic} -> {topic_name}")
        try:
            latest = SensorData.query.filter_by(topic=topic_name).order_by(desc(SensorData.timestamp)).first()
            logging.warning(f"Query result for '{topic_name}': {latest}")

            if data:
                # Create sanitized values list
                values = []
                for d in data:
                    if callable(d.value):
                        logging.warning(f"Found callable value in {topic_name} data: {d.value}")
                        # Convert function to string or use a default value
                        values.append(str(d.value))
                    elif isinstance(d.value, (dict, list, set)):
                        # Handle complex types that might contain functions
                        try:
                            # Test if JSON serializable
                            import json
                            json.dumps(d.value)
                            values.append(d.value)
                        except TypeError:
                            logging.warning(f"Found non-serializable complex value in {topic_name}")
                            values.append(str(d.value))
                    else:
                        values.append(d.value)

                sensor_data[topic_name] = {
                    'timestamps': [d.timestamp.strftime('%Y-%m-%d %H:%M:%S') for d in data],
                    'values': values
                }
                logging.info(f"Added sensor data for {topic_name} with {len(data)} points")
            else:
                logging.warning(f"No data found for {topic_name}")
        except Exception as e:
            logging.error(f"Error processing {topic_name}: {str(e)}")

    # Pass current time to template
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.warning(
        f"Rendering template with {len(latest_readings)} latest readings and {len(sensor_data)} sensor data series")

    return render_template('index.html',
                           readings=latest_readings,
                           sensor_data=sensor_data,
                           current_time=current_time)




