import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class StepperMotor:
    def __init__(self, step_pin, dir_pin, ms1_pin, ms2_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.ms1_pin = ms1_pin
        self.ms2_pin = ms2_pin

        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.ms1_pin, GPIO.OUT)
        GPIO.setup(self.ms2_pin, GPIO.OUT)

        self.set_resolution("FULL")

    def set_resolution(self, resolution):
        if resolution == "FULL":
            GPIO.output(self.ms1_pin, GPIO.LOW)
            GPIO.output(self.ms2_pin, GPIO.LOW)
        elif resolution == "HALF":
            GPIO.output(self.ms1_pin, GPIO.HIGH)
            GPIO.output(self.ms2_pin, GPIO.LOW)
        elif resolution == "QUARTER":
            GPIO.output(self.ms1_pin, GPIO.LOW)
            GPIO.output(self.ms2_pin, GPIO.HIGH)
        elif resolution == "EIGHTH":
            GPIO.output(self.ms1_pin, GPIO.HIGH)
            GPIO.output(self.ms2_pin, GPIO.HIGH)
        else:
            raise ValueError("Invalid resolution")

    def rotate(self, degrees, speed):
        steps = int(degrees / 0.9)
        delay = 1.0 / speed

        if degrees < 0:
            GPIO.output(self.dir_pin, GPIO.LOW)
        else:
            GPIO.output(self.dir_pin, GPIO.HIGH)

        for _ in range(steps):
            GPIO.output(self.step_pin, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.step_pin, GPIO.LOW)
            time.sleep(delay)

if __name__ == "__main__":
    try:
        motor = StepperMotor(step_pin=17, dir_pin=18, ms1_pin=19, ms2_pin=20)
        motor.rotate(360, 100)  # Rotate 360 degrees at a speed of 100 steps per second
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()
