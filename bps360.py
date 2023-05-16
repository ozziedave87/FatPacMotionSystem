import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class bipolarStepper():
    def __init__(self, pwmPinA=16, dirPinA=12, pwmPinB=21, dirPinB=20, RPM=10, stepsPerRotation=200):
        GPIO.setup(pwmPinA, GPIO.OUT)
        GPIO.setup(pwmPinB, GPIO.OUT)
        GPIO.setup(dirPinA, GPIO.OUT)
        GPIO.setup(dirPinB, GPIO.OUT)

        self.pwmA = GPIO.PWM(pwmPinA, 1000)
        self.pwmB = GPIO.PWM(pwmPinB, 1000)

        self.pwmA.start(100)
        self.pwmB.start(100)

        self.dirA = dirPinA
        self.dirB = dirPinB

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
            time.sleep(self.stepDelay_ms / 1000.0)
        while self.steps < 0:
            self.forwardStep()
            time.sleep(self.stepDelay_ms / 1000.0)

    def getSteps(self):
        return self.steps

    def getAngle(self):
        return self.steps % self.stepsPerRotation / self.stepsPerRotation * 360

    def forwardStep(self):
        GPIO.output(self.dirA, GPIO.HIGH)
        GPIO.output(self.dirB, GPIO.HIGH)
        self.steps += 1
        time.sleep(self.stepDelay_ms / 1000.0)

    def backwardStep(self):
        GPIO.output(self.dirA, GPIO.LOW)
        GPIO.output(self.dirB, GPIO.LOW)
        self.steps -= 1
        time.sleep(self.stepDelay_ms / 1000.0)

    def rotate(self, steps=0, angle=None):
        if angle is not None:
            steps = round(angle / 360.0 * self.stepsPerRotation)

        if steps < 0:
            while steps < 0:
                self.backwardStep()
                steps += 1
        else:
            while steps > 0:
                self.forwardStep()
                steps -= 1

    def stop(self):
        self.pwmA.stop()
        self.pwmB.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    try:
        stepper = bipolarStepper()
        stepper.rotate(steps=stepper.stepsPerRotation)
        time.sleep(1)
        stepper.rotate(steps=-stepper.stepsPerRotation)
        time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt")
    finally:
        stepper.stop()
        GPIO.cleanup()
        
