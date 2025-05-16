"""
GPIO Button Control with Threading and MQTT

This script sets up a button to toggle between two LEDs using a separate thread.
It utilizes the Raspberry Pi's GPIO library to control the pins and logs events.
It uses MQTT to receive and send messages that stear the LED's

Author: [Patrick D.]
Date: [15.03.25]
"""


import RPi.GPIO as GPIO
import time
import threading
import logging
import paho.mqtt.client as mqtt

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Set GPIO Mode
GPIO.setmode(GPIO.BCM)

# Define initial LED pin
led_pin = 24

# MQTT Configuration
MQTT_BROKER = "192.168.1.11"  # Replace with your broker address
MQTT_TOPIC_CONTROL = "home/led/controlRPiX" # Change X with your RPi Number
MQTT_TOPIC_STATUS = "home/led/statusRPiX" # Change X with your RPi Number

class Button:
    """Button handler running in a separate thread to detect presses."""
    def __init__(self, channel, mqtt_publisher):
        self.channel = channel
        self.mqtt_publisher = mqtt_publisher
        self._thread = threading.Thread(name='button', target=self.run)
        self._thread.daemon = True
        self._thread_active = True
        self._thread.start()

    def run(self):
        """Thread function to monitor button presses."""
        logger.info("Button thread started")
        previous = 1
        while self._thread_active:
            time.sleep(0.01)
            current = GPIO.input(self.channel)
            if current == 1 and previous == 0:
                logger.info("Button was pressed and released")
                self.on_button_press()
            previous = current

    def on_button_press(self):
        """Toggles the active LED pin."""
        global led_pin
        led_pin = 25 if led_pin == 24 else 24
        GPIO.output(24, False)
        GPIO.output(25, False)
        GPIO.output(led_pin, True)
        self.mqtt_publisher.publish_status(f"Button pressed, LED{led_pin} ON")

    def stop(self):
        """Stops the button thread."""
        self._thread_active = False

class MQTTPublisher:
    """MQTT Publisher to report LED status."""
    def __init__(self, broker, status_topic):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.status_topic = status_topic
        self.client.connect(broker, 1883, 60)

    def publish_status(self, message):
        logger.info(f"Publishing: {message}")
        self.client.publish(self.status_topic, message)

class MQTTListener:
    """MQTT Listener to control LED state based on messages."""
    def __init__(self, broker, topic, mqtt_publisher):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topic = topic
        self.mqtt_publisher = mqtt_publisher
        self._thread = threading.Thread(name='mqtt_listener', target=self.run)
        self._thread.daemon = True
        self._thread.start()

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected to MQTT broker")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        global led_pin
        payload = msg.payload.decode('utf-8')
        logger.info(f"MQTT Message Received: {payload}")
        if payload == "LED1_ON":
            led_pin = 24
            GPIO.output(24, True)
            GPIO.output(25, False)
            self.mqtt_publisher.publish_status(f"LED24 is ON and LED25 is OFF")
        elif payload == "LED2_ON":
            led_pin = 25
            GPIO.output(24, False)
            GPIO.output(25, True)
            self.mqtt_publisher.publish_status(f"LED24 is OFF and LED25 is ON")

    def run(self):
        self.client.connect(MQTT_BROKER, 1883, 60)
        self.client.loop_forever()

try:
    # Setup GPIO
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(24, GPIO.OUT)
    GPIO.setup(25, GPIO.OUT)
    GPIO.output(24, False)
    GPIO.output(25, False)

    mqtt_publisher = MQTTPublisher(MQTT_BROKER, MQTT_TOPIC_STATUS)
    button = Button(18, mqtt_publisher)
    mqtt_listener = MQTTListener(MQTT_BROKER, MQTT_TOPIC_CONTROL, mqtt_publisher)

    while True:
        GPIO.output(led_pin, True)
        time.sleep(1)
        GPIO.output(led_pin, False)
        time.sleep(1)
except KeyboardInterrupt:
    button.stop()
    logger.info("Stopping...")
    time.sleep(1)
    GPIO.cleanup()
