import cv2
import numpy as np
from defisheye import Defisheye

# Defisheye parameters
dtype = 'equalarea'
format = 'fullframe'
fov = 160
pfov = 107
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]

def nothing(x):
    pass

def selectGreen():
    data = np.loadtxt('Green_Threshold_Data.dat')
    data = np.asarray(data, dtype = 'int')
    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMin', 'image', data[0,0])
    cv2.setTrackbarPos('HMax', 'image', data[1,0])
    cv2.setTrackbarPos('SMin', 'image', data[0,1])
    cv2.setTrackbarPos('SMax', 'image', data[1,1])
    cv2.setTrackbarPos('VMin', 'image', data[0,2])
    cv2.setTrackbarPos('VMax', 'image', data[1,2])

def selectYellow():
    data = np.loadtxt('Yellow_Threshold_Data.dat')
    data = np.asarray(data, dtype = 'int')
    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMin', 'image', data[0,0])
    cv2.setTrackbarPos('HMax', 'image', data[1,0])
    cv2.setTrackbarPos('SMin', 'image', data[0,1])
    cv2.setTrackbarPos('SMax', 'image', data[1,1])
    cv2.setTrackbarPos('VMin', 'image', data[0,2])
    cv2.setTrackbarPos('VMax', 'image', data[1,2])

def selectPink():
    data = np.loadtxt('Pink_Threshold_Data.dat')
    data = np.asarray(data, dtype = 'int')
    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMin', 'image', data[0,0])
    cv2.setTrackbarPos('HMax', 'image', data[1,0])
    cv2.setTrackbarPos('SMin', 'image', data[0,1])
    cv2.setTrackbarPos('SMax', 'image', data[1,1])
    cv2.setTrackbarPos('VMin', 'image', data[0,2])
    cv2.setTrackbarPos('VMax', 'image', data[1,2])

def selectBlack():
    data = np.loadtxt('Black_Threshold_Data.dat')
    data = np.asarray(data, dtype = 'int')
    # Set default value for Max HSV trackbars
    cv2.setTrackbarPos('HMin', 'image', data[0,0])
    cv2.setTrackbarPos('HMax', 'image', data[1,0])
    cv2.setTrackbarPos('SMin', 'image', data[0,1])
    cv2.setTrackbarPos('SMax', 'image', data[1,1])
    cv2.setTrackbarPos('VMin', 'image', data[0,2])
    cv2.setTrackbarPos('VMax', 'image', data[1,2])
    

# Create a window
cv2.namedWindow('image')

# Create trackbars for color change
# Hue is from 0-179 for Opencv
cv2.createTrackbar('HMin', 'image', 0, 179, nothing)
cv2.createTrackbar('HMax', 'image', 179, 179, nothing)
cv2.createTrackbar('SMin', 'image', 0, 255, nothing)
cv2.createTrackbar('SMax', 'image', 255, 255, nothing)
cv2.createTrackbar('VMin', 'image', 0, 255, nothing)
cv2.createTrackbar('VMax', 'image', 255, 255, nothing)

cv2.createTrackbar('Colour', 'image', 0, 2, nothing)
prevCurrent = 4

# Initialize HSV min/max values
hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

cap = cv2.VideoCapture(0)

while(1):
    
    ret, frame = cap.read()
    # Load image
    obj = Defisheye(frame, dtype='linear', format=format, fov=fov, pfov=pfov)
    image = obj.convert()
    image = cv2.GaussianBlur(image, (7,7), 0)
    current = cv2.getTrackbarPos('Colour', 'image')
    
    if current == 0 and prevCurrent != 0:
        selectGreen()
        prevCurrent = 0
    elif current == 1 and prevCurrent != 1:
        selectYellow()
        prevCurrent = 1
    elif current == 2 and prevCurrent != 2:
        selectPink()
        prevCurrent = 2
    
    # Get current positions of all trackbars
    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')
    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')

    # Set minimum and maximum HSV values to display
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Convert to HSV format and color threshold
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    result = cv2.bitwise_and(image, image, mask=mask)

    # Print if there is a change in HSV value
    if((phMin != hMin) | (psMin != sMin) | (pvMin != vMin) | (phMax != hMax) | (psMax != sMax) | (pvMax != vMax) ):
        print("(hMin = %d , sMin = %d, vMin = %d), (hMax = %d , sMax = %d, vMax = %d)" % (hMin , sMin , vMin, hMax, sMax , vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    if current == 0:
        np.savetxt('Green_Threshold_Data.dat',[lower, upper])
    elif current == 1:
        np.savetxt('Yellow_Threshold_Data.dat',[lower, upper])
    elif current == 2:
        np.savetxt('Pink_Threshold_Data.dat',[lower, upper])
        
    # Display result image
    cv2.imshow('image', result)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
