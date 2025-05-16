# mqtt_client.py
import paho.mqtt.client as mqtt
from app import db
from app.models.sensors import SensorData
import threading
from flask import current_app


def on_connect(client, userdata, flags, rc):
    """Callback when client connects to MQTT broker"""
    if rc == 0:
        print("Connected to MQTT broker successfully")

        # Subscribe to all configured topics
        topics = current_app.config['MQTT_TOPICS']
        for topic in topics.keys():
            client.subscribe(topic)
            print(f"Subscribed to {topic}")
    else:
        print(f"Failed to connect to MQTT broker with code {rc}")


def on_message(client, userdata, msg):
    """Callback when message is received from MQTT broker"""
    topic = msg.topic

    try:
        # Try to decode and convert to float
        payload = msg.payload.decode('utf-8').strip()

        # Handle empty messages or special cases
        if not payload or topic in ["/smartroom9000/ventilation", "/smartroom9000/heating"]:
            value = 1.0  # Just record that something happened
        else:
            try:
                value = float(payload)
            except ValueError:
                value = 0.0

        # Store in database
        sensor_data = SensorData(topic=topic, value=value)
        db.session.add(sensor_data)
        db.session.commit()
        print(f"Stored data: {topic} = {value}")

    except Exception as e:
        print(f"Error processing MQTT message: {e}")


def start_mqtt_client(app):
    """Start the MQTT client in a background thread"""

    def run_mqtt_client():
        with app.app_context():
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_message = on_message

            # Connect to broker
            mqtt_broker = app.config['MQTT_BROKER']
            mqtt_port = app.config['MQTT_PORT']

            try:
                client.connect(mqtt_broker, mqtt_port, 60)
                client.loop_forever()
            except Exception as e:
                print(f"MQTT connection failed: {e}")

    # Start in a new thread
    mqtt_thread = threading.Thread(target=run_mqtt_client, daemon=True)
    mqtt_thread.start()
    print("MQTT client started in background thread")