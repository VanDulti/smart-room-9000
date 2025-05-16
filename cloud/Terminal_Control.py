from datetime import datetime

import paho.mqtt.client as mqtt
import time

# MQTT Configuration
MQTT_BROKER = "192.168.1.11"  # Replace with your broker address
MQTT_TOPIC_CONTROL = "home/led/controlRPiX" # Change X with your RPi Number
MQTT_TOPIC_STATUS = "home/led/statusRPiX" # Change X with your RPi Number

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(MQTT_TOPIC_STATUS)

def on_message(client, userdata, msg):
    print()
    print(f"Status Update: {msg.payload.decode('utf-8')}")

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start()
    time.sleep(1)
    
    while True:
        print("\nCommands:")
        print("1: Turn LED 1 ON")
        print("2: Turn LED 2 ON")
        print("q: Quit")
        
        cmd = input("Enter command: ")
        if cmd == "1":
            client.publish(MQTT_TOPIC_CONTROL, "LED1_ON")
        elif cmd == "2":
            client.publish(MQTT_TOPIC_CONTROL, "LED2_ON")
        elif cmd.lower() == "q":
            break
        else:
            print("Invalid command")
    
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    print("Listening for LED status updates...")
    main()


def store_measurement(timestamp: datetime, sensor: str, value: str):
    print(f'storing in db: {timestamp} {sensor} {value}')
