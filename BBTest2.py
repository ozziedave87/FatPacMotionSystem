# Imports
import RPi.GPIO as GPIO
import time

# Set up GPIO pin for the break beam sensor
Bay1BB_PIN = 17
GPIO.setup(Bay1BB_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to detect if pizza is in Bay 1
def Bay1BB_callback(channel):
    if GPIO.input(Bay1BB_PIN):
        print("Beam unbroken")
        Bay1BB_state = 0  # False
    else:
        print("Beam broken")
        Bay1BB_state = 1  # True

    # Do something with Bay1BB_state
    print("Bay1BB_state:", Bay1BB_state)

# Start break beams
GPIO.add_event_detect(Bay1BB_PIN, GPIO.BOTH, callback=Bay1BB_callback)  # For break beam sensor
