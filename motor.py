#motor drive module for dc motors with PWM and direction control using two pins on the pi
#with TC78H660FTG motor driver (Makerverse Motor Driver 2 Channel 
#https://core-electronics.com.au/makerverse-motor-driver-2-channel.html)
# David Keevers n10960317 EGH419

#Import and setup GPIO
import RPi.GPIO as GPIO
from time import sleep

#set pin numbering to BCM
GPIO.setmode(GPIO.BCM)

#Create motor class
class motor:
    def __init__(self, dir_pin, pwm_pin):
        self.dir_pin = dir_pin
        self.pwm_pin = pwm_pin
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pwm_pin, 1000)
        self.pwm.start(0)
        self.dir = 0
        self.speed = 0
    #set direction
    def set_dir(self, dir):
        self.dir = dir
        GPIO.output(self.dir_pin, self.dir)

    #set speed
    def set_speed(self, speed):
        self.speed = speed
        self.pwm.ChangeDutyCycle(self.speed)

    #set stop
    def stop(self):
        self.set_speed(0)

    #drive forward
    def forward(self, speed):
        self.set_dir(0)
        self.set_speed(speed)

    #drive in reverse
    def reverse(self, speed):
        self.set_dir(1)
        self.set_speed(speed)

    #destructor
    def __del__(self):
        self.pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)
        motor1 = motor(10, 9)
        motor1.forward(100)
        sleep(2)
        motor1.reverse(100)
        sleep(2)
        motor1.stop()
        sleep(2)

        motor2 = motor(27, 22)
        motor2.forward(100)
        sleep(2)
        motor2.stop()
        sleep(2)

    except KeyboardInterrupt:   # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt") 
    finally:
        GPIO.cleanup()







