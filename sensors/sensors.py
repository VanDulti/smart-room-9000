import time
import board
import busio
import RPi.GPIO as GPIO

# Import the mqtt_client module
from mqtt_sub import publish_sensor_data

# Adafruit sensors
import adafruit_sht31d
import adafruit_veml7700

# MQTT Configuration
MQTT_HOST = "pi4felix.local"
MQTT_PORT = 1883

# Setup GPIO for PIR
PIR_PIN = 12
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# initialize other sensors
sht31 = adafruit_sht31d.SHT31D(i2c)
veml7700 = adafruit_veml7700.VEML7700(i2c)

# main loop
try:
    while True:
        # read sensor data
        temperature = sht31.temperature
        humidity = sht31.relative_humidity
        lux = veml7700.lux
        motion = GPIO.input(PIR_PIN)  # 1 = motion detected, 0 = no motion

        # Send data to MQTT broker
        publish_sensor_data(MQTT_HOST, MQTT_PORT, "temperature", temperature)
        publish_sensor_data(MQTT_HOST, MQTT_PORT, "humidity", humidity)
        publish_sensor_data(MQTT_HOST, MQTT_PORT, "ambientlight", lux)
        publish_sensor_data(MQTT_HOST, MQTT_PORT, "mmwave", 1 if motion else 0)

        # Print sensor data to console
        print("\nSensor data:")
        print(f"  Temperature:      {temperature:.2f} °C")
        print(f"  Humidity:{humidity:.2f} %")
        print(f"  Light:     {lux:.2f} Lux")
        print(f"  Motion:        {'Yes' if motion else 'No'}")
        print("-" * 40)
        time.sleep(2)

except KeyboardInterrupt:
    print("\nTerminating program...")

finally:
    GPIO.cleanup()