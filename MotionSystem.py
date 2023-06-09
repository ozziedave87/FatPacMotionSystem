#Motion system for FatPac pizza topping robot
#David Keevers n10960317 EGH419

#Import and setup GPIO
import RPi.GPIO as GPIO
from time import sleep
import motor
import stepper

#set pin numbering to BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

############################### Sensor Set up #################################
#set up break beams
BBSauce_Pin = 2
BBTopping_Pin = 3

#set pin for break bream sensor 
GPIO.setup(BBSauce_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(BBTopping_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#initialise break beam states
sauceBay_state = None
toppingBay_state = None

#function for break beam for ram positioning
def sauce_callback(channel):
    if GPIO.input(BBSauce_Pin):
        #print("beam unbroken")
        sauceBay_state = 0         #false
    else:
        #print("beam broken")
        sauceBay_state = 1         #true

def topping_callback(channel):
    if GPIO.input(BBTopping_Pin):
        #print("beam unbroken")
        toppingBay_state = 0         #false
    else:
        #print("beam broken")
        toppingBay_state = 1         #true
        
#start break beams
GPIO.add_event_detect(BBSauce_Pin, GPIO.BOTH, callback=sauce_callback) 
GPIO.add_event_detect(BBTopping_Pin, GPIO.BOTH, callback=topping_callback) 

#set up limit switches
LSUp_Pin = 4
LSDown_Pin = 14

GPIO.setup(LSUp_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Set pin for limit switch and enable input and pull up resistors
GPIO.setup(LSDown_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Set pin for limit switch and enable input and pull up resistors

########################### Conveyor Set up ###################################
ConveyorDir_Pin = 10
ConveyorPWM_Pin = 9

#initialise conveyor motor
Conveyor = motor.motor(ConveyorDir_Pin, ConveyorPWM_Pin)

################################ Ram Set up ###################################
RamPWM_Pin = 1
RamDir_Pin = 22

#initialise ram motor
Ram = motor.motor(RamDir_Pin, RamPWM_Pin)

#initialise ram states
#RamUp_state = None
#RamDown_state = None
RamUp_state = GPIO.input(LSUp_Pin) #limit switch - read and store value of input to a variable
RamDown_state = GPIO.input(LSDown_Pin) #limit switch - read and store value of input to a variable

############################### Stepper Set up #################################
SpinnerDirA_Pin = 15
SpinnerPWMA_Pin = 17
SpinnerDirB_Pin = 18
SpinnerPWMB_Pin = 22

#initialise stepper motor
Spinner = stepper.StepperMotor(SpinnerDirA_Pin, SpinnerPWMA_Pin, SpinnerDirB_Pin, SpinnerPWMB_Pin)

############################### Global Variables #################################
global motionInit_state
global saucing_state
global topping_state


#ram up function
def ramUp():
    if RamUp_state == 0:
        while RamUp_state == 0:
            Ram.forward(100)
            print('ram going up')
        print('ram up')
    elif RamUp_state == 1:
        Ram.stop()
        print('ram already up')

#ram down function
def ramDown():
    if RamDown_state == 0:
        while RamDown_state == 0:
            Ram.reverse(100)
            print('ram  going down')
        print('ram down')
    elif RamDown_state == 1:
        Ram.stop()
        print('ram already down')

#ram home function
def ramHome():
    ramDown()
    Ram.forward(100)
    sleep(2) #time for ram to reach home position
    Ram.stop()

#create initialization function for startup - ensure fatpac is in a safe operaitonal state
def motionInit():
#    motionInit_state = None #init state for start up
    #check bay is clear
    if sauceBay_state and toppingBay_state == 0:
        ramHome()
        motionInit_state = 1 #intialization complete
        print('bays are clear and FatPac is ready to make a pizza')
    elif sauceBay_state or toppingBay_state == 1:
        motionInit_state = 0 #initialization incomplete
        print('FatPac is not ready to make a pizza - check bays for obstructions')
    return motionInit_state

#create function for saucing
def saucing():
#    saucing_state = 0 #init state for saucing
    if sauceBay_state == 1:
        try:
            ramUp()
            sleep(1.5) #time for sauce to dispense
            Spinner.rotate(1, 600, 540) #direction, rpm, rotation
            sleep(0.5) #time for sauce to settle
            ramDown()
            saucing_state = 1 #saucing complete
        except:
            saucing_state = 0 #saucing incomplete
            print('error - something has gone wrong with saucing')
    else:
        saucing_state = 0 #saucing incomplete
        print('error - no pizza base has been detected in the sauce bay')
    return saucing_state

#fucntion to transition between sauce and topping bay
def baseToTopping():
#    saucing_state = 1 #for testing purposes
    if saucing_state == 1:
        try:
            while toppingBay_state == 0:
                Conveyor.forward(100)
                print('base going to topping bay')
            #reset saucing bay and state
            ramHome()
            saucing_state = 0
        except:
            saucing_state = 1
            print('error - check topping bay for obstructions') #or another pizza is being topped
    else:
        print('error - saucing not complete')
        saucing_state = 1
    return saucing_state

#create function for finishing
#conditional on QC
def pizzaUnload(): 
    try:
        while toppingBay_state == 1:
            Conveyor.forward(100)
            print('pizza is ready for baking')
    except:
        print('error - something has gone wrong with finishing the pizza')
    else:
        print('error - no pizza has been detected in the topping bay or sauce bay is full')

###################################################################################
################################ Subsystem testing ################################
###################################################################################
if __name__ == "__main__":
    try:
        print('starting up - motionInit')
        motionInit()
        print(motionInit_state)
        sleep(1)
        print('saucing')
        saucing()
        sleep(1)
        print(saucing_state)
        print('base to topping')
        baseToTopping()
        sleep(1)
        print('pizza finish')
        pizzaUnload()
        sleep(1)

    except KeyboardInterrupt:   # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")
    finally:
        GPIO.cleanup()