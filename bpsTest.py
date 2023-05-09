#create test mdoule for bipolar stepper

import RPi.GPIO as GPIO
from time import sleep
import bipolarStepper as bps

GPIO.setmode(GPIO.BCM)

#set up pins
pwmPinA = 17
dirPinA = 18
pwmPinB = 19
dirPinB = 20

#set up stepper
stepper = bps.bipolarStepper(pwmPinA, dirPinA, pwmPinB, dirPinB, 10, 200)

#test stepper
stepper.forwardStep()
sleep(0.5)
stepper.backwardStep()
sleep(0.5)
StepperSauce.rotate(180)
sleep(2)
StepperSauce.rotate(-180)
sleep(2)