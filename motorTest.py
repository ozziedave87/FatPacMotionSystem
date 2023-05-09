#Test motor.py in another module

import RPi.GPIO as GPIO
from time import sleep
import motor

print("Testing MD2.py")

if __name__ == "__main__":
    try:
        #initialise motor 1
        GPIO.setmode(GPIO.BCM)
        MotorConveyor = motor.motor(20, 21)
        MotorConveyor.forward(100)
        sleep(2)
        MotorConveyor.reverse(100)
        sleep(2)
        MotorConveyor.stop()
        sleep(2)
    except KeyboardInterrupt:   # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()