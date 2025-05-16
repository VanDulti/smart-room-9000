import RPi.GPIO as GPIO
import time
import threading
import logging

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level="INFO")

# Set GPIO Mode
GPIO.setmode(GPIO.BCM)  # Using BCM mode for pin numbering

# Define initial LED pin
led_pin = 24

class Button:
    """Button handler running in a separate thread to detect presses."""
    def __init__(self, channel):
        self.channel = channel
        self._thread = threading.Thread(name='button', target=self.run)
        self._thread.daemon = True  # Ensures the thread exits when the program terminates
        self._thread_active = True
        self._thread.start()

    def run(self):
        """Thread function to monitor button presses."""
        logger.info("Button thread started")
        previous = 1  # Previous button state (default: not pressed)
        while self._thread_active:
            time.sleep(0.01)  # Small delay to prevent CPU overuse
            current = GPIO.input(self.channel)
            logger.debug("Current: %s, Previous: %s", current, previous)
            
            if current == 1 and previous == 0:
                logger.info("Button was pressed and released")
                self.on_button_press()
            
            previous = current

    def on_button_press(self):
        """Toggles the active LED pin."""
        global led_pin
        led_pin = 25 if led_pin == 24 else 24  # Toggle LED pin
        GPIO.output(24, False)  # Turn off both LEDs
        GPIO.output(25, False)

    def stop(self):
        """Stops the button thread."""
        logger.debug("Stopping thread")
        self._thread_active = False

try:
    # Setup GPIO
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Button input with pull-up resistor
    button = Button(18)
    
    GPIO.setup(24, GPIO.OUT)  # LED 1
    GPIO.setup(25, GPIO.OUT)  # LED 2
    GPIO.output(24, False)  # Initial state OFF
    GPIO.output(25, False)  # Initial state OFF

    while True:
        # Toggle the active LED
        GPIO.output(led_pin, True)
        time.sleep(1)
        GPIO.output(led_pin, False)
        time.sleep(1)
except KeyboardInterrupt:
    button.stop()
    logger.info("Stopping...")
    time.sleep(1)
    GPIO.cleanup()  # Cleanup GPIO settings on exit
