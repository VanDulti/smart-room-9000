import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///smartroom.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MQTT configurations
    MQTT_BROKER = "pi4felix.local"
    MQTT_PORT = 1883

    # MQTT Topics
    MQTT_TOPICS = {
        "/smartroom9000/mmwave": "mmwave",
        "/smartroom9000/ambientlight": "ambientlight",
        "/smartroom9000/humidity": "humidity",
        "/smartroom9000/temperature": "temperature",
        "/smartroom9000/ventilation": "ventilation",
        "/smartroom9000/heating": "heating",
        "/smartroom9000/lightcontrol": "light_control"
    }