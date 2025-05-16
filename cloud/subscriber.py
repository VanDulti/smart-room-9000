import paho.mqtt.client as mqtt
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# MQTT Configuration
MQTT_HOST = "pi4felix.local"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC_MMWAVE = "/smartroom9000/mmwave" # ???
MQTT_TOPIC_AMBIENTLIGHT = "/smartroom9000/ambientlight" # brightness
MQTT_TOPIC_HUMIDITY = "/smartroom9000/humidity" # percent float
MQTT_TOPIC_TEMPERATURE = "/smartroom9000/temperature" # deg
MQTT_TOPIC_VENTILATION = "/smartroom9000/ventilation" # empty message
MQTT_TOPIC_HEATING = "/smartroom9000/heating" # empty message
MQTT_TOPIC_LIGHT_CONTROL = "/smartroom9000/lightcontrol" # brightness float

# Define on_connect event Handler
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker successfully")
        if MQTT_TOPIC_MMWAVE:
            client.subscribe(MQTT_TOPIC_MMWAVE, qos=0)
        else:
            logging.warning("MQTT_TOPIC is empty. Subscription skipped.")
    else:
        logging.error(f"Failed to connect, return code {rc}")

# Define on_subscribe event Handler
def on_subscribe(client, userdata, mid, granted_qos):
    logging.info(f"Subscribed to MQTT Topic: {MQTT_TOPIC_MMWAVE} with QoS {granted_qos}")

# Define on_message event Handler
def on_message(client, userdata, msg):
    logging.info(f"Received Message: {msg.payload.decode()} from Topic: {msg.topic}")

# Initialize MQTT Client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Register Event Handlers
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message

try:
    # Connect to MQTT Broker
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)
    
    # Start the network loop
    mqttc.loop_forever()

except Exception as e:
    logging.error(f"MQTT Error: {e}")
