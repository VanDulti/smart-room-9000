import threading
from datetime import datetime

from webservice.app import db
from webservice.app.models.sensors import SensorData
from webservice.app.services.mqtt_sub import start_mqtt_client


def start_mqtt_service():
    def actual():
        start_mqtt_client(host='pi4felix.local', port=1883, on_data=store_measurement)
    thread = threading.Thread(target=actual)
    thread.daemon = True  # Ensures the thread exits when the program terminates
    thread.start()
    print("MQTT service started in a separate thread.")


def store_measurement(timestamp: datetime, sensor: str, value: float):
     print(f'storing in db: {timestamp} {sensor} {value}')
     sensor_data = SensorData(timestamp=timestamp, topic=sensor, value=value)
     db.session.add(sensor_data)
     db.session.commit()