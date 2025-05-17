import threading
from datetime import datetime
from smartroom_mqtt import start_mqtt_client


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
    from webservice.app.models.sensors import SensorData
    sensor_data = SensorData(timestamp=timestamp, topic=sensor, value=value)
    with app.app_context():
        app.db.session.add(sensor_data)
        app.db.session.commit()
