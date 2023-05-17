#Test stepper.py in another module

import RPi.GPIO as GPIO
from time import sleep
import stepper

print("Testing stepper.py")

if __name__ == "__main__":
    try:
        #initialise motor 1
        GPIO.setmode(GPIO.BCM)
        StepperSauce = stepper.stepper(20, 21, 22, 23)
        StepperSauce.forward(100)
        sleep(2)
        StepperSauce.reverse(100)
        sleep(2)
        StepperSauce.stop()
        sleep(2)
    except KeyboardInterrupt:   # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()
