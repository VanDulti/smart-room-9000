import paho.mqtt.client as mqtt
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# MQTT Configuration
MQTT_HOST = "pi4felix.local"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 5
MQTT_TOPIC = "/topic/RPiX"
MQTT_MSG = "Hello from RPiX"  # Example message

# Define on_connect event Handler
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT Broker successfully")
    else:
        logging.error(f"Failed to connect, return code {rc}")

# Define on_publish event Handler
def on_publish(client, userdata, mid):
    logging.info("Message Published successfully")

# Initialize MQTT Client
mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)


# Register Event Handlers
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

try:
    # Connect to MQTT Broker
    mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

    # Start MQTT loop to handle callbacks
    mqttc.loop_start()

    # Ensure Topic and Message are valid before publishing
    if MQTT_TOPIC and MQTT_MSG:
        mqttc.publish(MQTT_TOPIC, MQTT_MSG)
    else:
        logging.warning("MQTT_TOPIC or MQTT_MSG is empty, skipping publish")

    # Give some time for message to be sent before disconnecting
    mqttc.loop_stop()
    mqttc.disconnect()

except Exception as e:
    logging.error(f"Error: {e}")
