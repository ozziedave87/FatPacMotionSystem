#create motor drive module stepper motors with PWM and direction control using four pins on the pi
# with TC78H660FTG motor driver (Makerverse Motor Driver 2 Channel https://core-electronics.com.au/makerverse-motor-driver-2-channel.html)

#Import and setup GPIO
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

class motor:
    def __init__(self, dir_a_pin, pwm_a_pin, dir_b_pin, pwm_b_pin):
        self.dir_a_pin = dir_a_pin
        self.pwm_a_pin = pwm_a_pin
        self.dir_b_pin = dir_b_pin
        self.pwm_b_pin = pwm_b_pin

        GPIO.setup(self.dir_a_pin, GPIO.OUT)
        GPIO.setup(self.pwm_a_pin, GPIO.OUT)
        GPIO.setup(self.dir_b_pin, GPIO.OUT)
        GPIO.setup(self.pwm_b_pin, GPIO.OUT)

        self.pwm_a = GPIO.PWM(self.pwm_a_pin, 1000)
        self.pwm_b = GPIO.PWM(self.pwm_b_pin, 1000)

        self.pwm_a.start(0)
        self.pwm_b.start(0)

        self.dir_a = 0
        self.speed_a = 0
        self.dir_b = 0
        self.speed_b = 0

    def set_dir_a(self, dir):
        self.dir_a = dir
        GPIO.output(self.dir_a_pin, self.dir_a)

    def set_speed_a(self, speed):
        self.speed_a = speed
        self.pwm_a.ChangeDutyCycle(self.speed_a)

    def set_dir_b(self, dir):
        self.dir_b = dir
        GPIO.output(self.dir_b_pin, self.dir_b)

    def set_speed_b(self, speed):
        self.speed_b = speed
        self.pwm_b.ChangeDutyCycle(self.speed_b)

    def stop(self):
        self.set_speed_a(0)
        self.set_speed_b(0)

    def forward(self, speed):
        self.set_dir_a(0)
        self.set_dir_b(0)
        self.set_speed_a(speed)
        self.set_speed_b(speed)

    def reverse(self, speed):
        self.set_dir_a(1)
        self.set_dir_b(1)
        self.set_speed_a(speed)
        self.set_speed_b(speed)

    def __del__(self):
        self.pwm_a.stop()
        self.pwm_b.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        motor1 = motor(20, 21, 22, 23)
        motor1.forward(100)
        sleep(2)
        motor1.reverse(100)
        sleep(2)
        motor1.stop()
        sleep(2)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()
