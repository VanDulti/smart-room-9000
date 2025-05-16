# mqtt_client.py
from datetime import datetime
from typing import Callable, Any

import paho.mqtt.client as mqtt
import threading
from flask import current_app
from paho.mqtt.client import MQTTMessage, Client

MQTT_KEEPALIVE_INTERVAL = 5

MQTT_TOPICS = {
    "/smartroom9000/motion": "motion",
    "/smartroom9000/ambientlight": "ambientlight",
    "/smartroom9000/humidity": "humidity",
    "/smartroom9000/temperature": "temperature",
    "/smartroom9000/ventilation": "ventilation",
    "/smartroom9000/heating": "heating",
    "/smartroom9000/lightcontrol": "light_control"
}


def on_connect(client, userdata, flags, rc):
    """Callback when client connects to MQTT broker"""
    if rc == 0:
        print("Connected to MQTT broker successfully")

        # Subscribe to all configured topics
        topics = MQTT_TOPICS.keys()
        for topic in topics:
            client.subscribe(topic)
            print(f"Subscribed to {topic}")
    else:
        print(f"Failed to connect to MQTT broker with code {rc}")


def create_on_message(on_data: Callable[[datetime, str, float], None]) -> Callable[[Client, Any, MQTTMessage], None]:
    def on_message(client: Client, userdata: Any, msg: MQTTMessage):
        """Callback when message is received from MQTT broker"""
        topic = msg.topic
        try:
            # Try to decode and convert to float
            payload = msg.payload.decode('utf-8').strip()

            sensor = MQTT_TOPICS.get(topic)
            if sensor is None:
                print(f"Unknown topic: {topic}")
                return

            try:
                value = float(payload)
            except ValueError:
                print(f"Invalid value for {sensor}: {payload}")
                return

            # Store in database
            on_data(datetime.now(), sensor, value)

        except Exception as e:
            print(f"Error processing MQTT message: {e}")

    return on_message


def start_mqtt_client(host: str, port: int, on_data: Callable[[datetime, str, float], None]):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = create_on_message(on_data)

    # Connect to broker
    mqtt_broker = host
    mqtt_port = port

    try:
        client.connect(mqtt_broker, mqtt_port, 60)
        res = client.loop_forever()
    except Exception as e:
        print(f"MQTT connection failed: {e}")


def publish_sensor_data(host: str, port: int, sensor: str, value: float):
    """Publish sensor data to MQTT broker"""
    client = mqtt.Client()
    client.connect(host, port, 60)
    topic = f"/smartroom9000/{sensor}"
    client.publish(topic, value)
    client.disconnect()


if __name__ == '__main__':
    # Example usage
    def example_on_data(timestamp: datetime, sensor: str, value: float):
        print(f"Received data: {timestamp} {sensor} {value}")


    start_mqtt_client("pi4felix.local", 1883, example_on_data)
