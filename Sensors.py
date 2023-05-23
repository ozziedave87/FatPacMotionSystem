#Sources
#Limit switch: https://electrosome.com/using-switch-raspberry-pi/
#Break beam: https://simonprickett.dev/using-a-break-beam-sensor-with-python-and-raspberry-pi/

#Imports
import RPi.GPIO as GPIO
import time
from time import sleep #VSC wants this specifically, shouldnt be needed

# initialisation
GPIO.setmode(GPIO.BCM)	 	     	# set the GPIO pin naming convention to BCM

#Set pins and setup
UpLs_PIN = 4 
DownLS_PIN = 14
Bay1BB_PIN = 2 
Bay2BB_PIN = 3

GPIO.setup(UpLs_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Set pin for limit switch and enable input and pull up resistors
GPIO.setup(DownLS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Set pin for limit switch and enable input and pull up resistors
GPIO.setup(Bay1BB_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin for break bream sensor 
GPIO.setup(Bay2BB_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) #set pin for break bream sensor

#function to detect if ram is up
def UpLs_sensor():
    print('UpLs_sensor called')
    while True:
      input_state = GPIO.input(UpLs_PIN) #Read and store value of input to a variable
      if input_state == False:     #Check whether pin is grounded
         print('success - lift is up')
         time.sleep(0.3)           #Delay of 0.3s
         UpLs_state = 1         #true
         break
      else:
        print('Lift is not up')
        time.sleep(0.3)           #Delay of 0.3s
        UpLs_state = 0         #false
        break
    return UpLs_state

#function to detect if ram is down
def DownLS_sensor():
    print('DownLS_sensor called')
    while True:
      input_state = GPIO.input(DownLS_PIN) #Read and store value of input to a variable
      if input_state == False:     #Check whether pin is grounded
         print('success - lift is down')
         time.sleep(0.3)           #Delay of 0.3s
         DownLS_state = 1         #true
         break
      else:
        print('Lift is not down')
        time.sleep(0.3)           #Delay of 0.3s
        DownLS_state = 0         #false
        break
    return DownLS_state

#function to detect if pizza is in Bay 1
def Bay1BB_callback(channel):
    if GPIO.input(Bay1BB_PIN):
        print("beam unbroken")
        Bay1BB_state = 0         #false
    else:
        print("beam broken")
        Bay1BB_state = 1         #true
    return Bay1BB_state

#function to detect if pizza is in Bay 2
def Bay2BB_callback(channel):
    if GPIO.input(Bay2BB_PIN):
        print("beam unbroken")
        Bay2BB_state = 0         #false
    else:
        print("beam broken")
        Bay2BB_state = 1         #true
    return Bay2BB_state

        
#start break beams
GPIO.add_event_detect(Bay1BB_PIN, GPIO.BOTH, callback=Bay1BB_callback) #for breakbeam sensor
GPIO.add_event_detect(Bay2BB_PIN, GPIO.BOTH, callback=Bay2BB_callback) #for breakbeam sensor

########################################################################################
###########-----~~~~~~~~~-----TESTING CODE------~~~~~~~---------########################
########################################################################################


if __name__=="__main__": 
    try:
       while True:
          #UpLs_sensor()
          #DownLS_sensor()
          Bay1BB_callback()
          Bay2BB_callback()
          sleep(0.5)           #Delay of 0.5s

    except:
        print("Legoman is sad and everything is broken")
        pass #this is good coding practice, fail silently.... 


    print("clean up") 
    GPIO.cleanup() # cleanup all GPIO 