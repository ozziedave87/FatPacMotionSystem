#Stepper motor control module control using four pins on the pi
# with TC78H660FTG motor driver (Makerverse Motor Driver 2 Channel 
#https://core-electronics.com.au/makerverse-motor-driver-2-channel.html)

#code adapted from http:///www.electronicwings.com

#imports
import RPi.GPIO as GPIO
from time import sleep

#Create stepper class
class StepperMotor:
    def __init__(self, dirA, pwmA, dirB, pwmB, stepsPerRotation=200): #360/1.8 = 200
        self.dirA = dirA
        self.pwmA = pwmA
        self.dirB = dirB
        self.pwmB = pwmB
        self.stepsPerRotation = stepsPerRotation
        GPIO.setwarnings(False)
        #set pin numbering to BCM
        GPIO.setmode(GPIO.BCM)
        GPIO.setup((self.dirA, self.pwmA, self.dirB, self.pwmB), GPIO.OUT)

#create direction contorl; clockwie and anticlockwise
    def set_direction(self, direction):
        if direction == 1: # clockwise
            GPIO.output((self.dirA, self.pwmA, self.dirB, self.pwmB), (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
            sleep(self.ts)
            GPIO.output((self.dirA, self.pwmA, self.dirB, self.pwmB), (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
            sleep(self.ts)
            GPIO.output((self.dirA, self.pwmA, self.dirB, self.pwmB), (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
            sleep(self.ts)
            GPIO.output((self.dirA, self.pwmA, self.dirB, self.pwmB), (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
            sleep(self.ts)
        elif direction == 0: #anticlockwise
            GPIO.output((self.dirA, self.pwmA, self.dirB, self.pwmB), (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
            sleep(self.ts)
            GPIO.output((self.dirA, self.pwmA, self.dirB, self.pwmB), (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.HIGH))
            sleep(self.ts)
            GPIO.output((self.dirA, self.pwmA, self.dirB, self.pwmB), (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
            sleep(self.ts)
            GPIO.output((self.dirA, self.pwmA, self.dirB, self.pwmB), (GPIO.HIGH, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
            sleep(self.ts)
        #error handling
        else:
            raise ValueError("Invalid direction. Must be 'clockwise' or 'anticlockwise'.")

#create user input for direction, rpm and rotation
    def rotate(self, dir, rpm, rotation):
        self.ts = 3600 / (rpm * self.stepsPerRotation)
        steps = int(rotation / (1.8 * 4))
        motor_direction = dir


#create loop that runs stepper for numbers of steps calculated by rotation input
        for _ in range(steps):
            try:
                if motor_direction == 1: #clockwise
                    print('Motor running clockwise')
                    self.set_direction(1)

                elif motor_direction == 0: #anticlockwise
                    print('Motor running anticlockwise')
                    self.set_direction(0)

            #error handling
            except KeyboardInterrupt:
                motor_direction = input("Select motor direction (0=anticlockwise, 1=clockwise) or q=exit: ")
                if motor_direction == 'q':
                    print('Motor stopped')
                    break

            


# Usage example:
if __name__ == '__main__':
    try:
        motor = StepperMotor(dirA=12, pwmA=16, dirB=21, pwmB=20)
        motor.rotate(dir = 1, rpm=600, rotation=180)
    except KeyboardInterrupt:
        print('Motor stopped')
    finally:
        GPIO.cleanup()
