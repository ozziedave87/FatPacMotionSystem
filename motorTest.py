#David Keevers n10960317 EGH419

import RPi.GPIO as GPIO
from time import sleep
import motor



if __name__ == "__main__":
    try:
        
    except KeyboardInterrupt:   # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()