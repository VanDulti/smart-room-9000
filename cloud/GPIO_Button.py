import RPi.GPIO as GPIO
from time import sleep
import logging

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

# set GPIO Mode 
GPIO.setmode(GPIO.BCM)  # Using BCM mode for pin numbering

# setup GPIO pins
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input with pull-up resistor
GPIO.setup(24, GPIO.OUT)  # Output pin for LED or device
GPIO.setup(25, GPIO.OUT)  # Another output pin for LED or device
GPIO.output(24, False)  # Initial state OFF
GPIO.output(25, False)  # Initial state OFF

active_pin = 24  # Default active pin

try:
     while True:
          button_state = GPIO.input(18)  # Read button state
          logger.info("button state is %s (pressed=%s)", button_state, not bool(button_state))
      # Choose which pin to activate based on button state
          if not button_state:
               active_pin = 24  # Assign pin based on button press
          else: 
               active_pin = 25
          GPIO.output(active_pin, True)  # Turn on selected pin
          sleep(1)
          GPIO.output(active_pin, False)  # Turn off selected pin
          sleep(1)
except KeyboardInterrupt: 
    logger.info("cleaning up ...")
    GPIO.cleanup()  # Cleanup GPIO settings on exit
