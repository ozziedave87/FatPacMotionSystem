#create test mdoule for bipolar stepper

import RPi.GPIO as GPIO
from time import sleep
import bipolarStepper as bps

GPIO.setmode(GPIO.BCM)

#set up pins
pwmPinA = 16
dirPinA = 12
pwmPinB = 21
dirPinB = 20

#set up stepper
stepper = bps.bipolarStepper(pwmPinA, dirPinA, pwmPinB, dirPinB, 10, 200)

#test stepper
stepper.forwardStep()
sleep(2)
stepper.backwardStep()
sleep(2)
print('end T1')
stepper.rotate(180)
sleep(2)
stepper.rotate(-180)
sleep(2)
print('end T2')