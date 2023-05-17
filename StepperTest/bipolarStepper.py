#create stepper drive module with PWM, direction and angle of rotation control using four pins on the pi
# with TC78H660FTG motor driver (Makerverse Motor Driver 2 Channel https://core-electronics.com.au/makerverse-motor-driver-2-channel.html)

#Import and setup GPIO
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

class bipolarStepper:
    def __init__(self, pwmPinA, dirPinA, pwmPinB, dirPinB, RPM=10, stepsPerRotation=200):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pwmPinA, GPIO.OUT)
        GPIO.setup(pwmPinB, GPIO.OUT)
        GPIO.setup(dirPinA, GPIO.OUT)
        GPIO.setup(dirPinB, GPIO.OUT)

        self.pwmA = GPIO.PWM(pwmPinA, 1000)
        self.pwmB = GPIO.PWM(pwmPinB, 1000)
        self.dirA = dirPinA
        self.dirB = dirPinB

        self.pwmA.start(0)
        self.pwmB.start(0)
        GPIO.output(self.dirA, GPIO.HIGH)
        GPIO.output(self.dirB, GPIO.HIGH)

        self.next = "A"

        self.steps = 0

        self.stepDelay_ms = int(60000 / (RPM * stepsPerRotation))

        self.RPM = RPM
        self.stepsPerRotation = stepsPerRotation

    def setRPM(self, RPM):
        self.stepDelay_ms = int(60000 / (RPM * self.stepsPerRotation))

    def setHome(self):
        self.steps = 0

    def returnHome(self):
        while self.steps > 0:
            self.backwardStep()
            sleep(self.stepDelay_ms / 1000)
        while self.steps < 0:
            self.forwardStep()
            sleep(self.stepDelay_ms / 1000)

    def getSteps(self):
        return self.steps

    def getAngle(self):
        return self.steps % self.stepsPerRotation / self.stepsPerRotation * 360

    def forwardStep(self):
        if self.next == "A":
            if GPIO.input(self.dirA):
                GPIO.output(self.dirA, GPIO.LOW)
            else:
                GPIO.output(self.dirA, GPIO.HIGH)
            self.next = "B"
        else:
            if GPIO.input(self.dirB):
                GPIO.output(self.dirB, GPIO.LOW)
            else:
                GPIO.output(self.dirB, GPIO.HIGH)
            self.next = "A"
        self.steps += 1

    def backwardStep(self):
        if self.next == "A":
            if GPIO.input(self.dirB):
                GPIO.output(self.dirB, GPIO.LOW)
            else:
                GPIO.output(self.dirB, GPIO.HIGH)
            self.next = "B"
        else:
            if GPIO.input(self.dirA):
                GPIO.output(self.dirA, GPIO.LOW)
            else:
                GPIO.output(self.dirA, GPIO.HIGH)
            self.next = "A"
        self.steps -= 1

    def rotate(self, steps=0, angle=None):
        if angle is not None:
            steps = round(angle / 360.0 * self.stepsPerRotation)

        if steps < 0:
            while steps < 0:
                self.backwardStep()
                steps += 1
                sleep(self.stepDelay_ms / 1000)
        else:
            while steps > 0:
                self.forwardStep()
                steps -= 1
                sleep(self.stepDelay_ms / 1000)

    def __del__(self):
        self.pwmA.stop()
        self.pwmB.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        #initialise motor 1
        StepperSauce = bipolarStepper(17, 18, 19, 20, 10, 200)
        StepperSauce.rotate(180)
        sleep(2)
        StepperSauce.rotate(-180)
        sleep(2)
        StepperSauce.rotate(360)
        sleep(2)
        StepperSauce.rotate(-360)
        sleep(2)


    except KeyboardInterrupt:   # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()