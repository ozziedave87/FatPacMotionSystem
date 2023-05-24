import numpy as np
import cv2
from defisheye import Defisheye

# Defisheye parameters
dtype = 'equalarea'
format = 'fullframe'
fov = 160
pfov = 107
flags = [i for i in dir(cv2) if i.startswith('COLOR_')]

# Threshold boundaries
green_data = np.loadtxt('Green_Threshold_Data.dat')
green_data = np.asarray(green_data, dtype = 'int')
lower_green = green_data[0,0:3]
upper_green = green_data[1,0:3]

yellow_data = np.loadtxt('Yellow_Threshold_Data.dat')
yellow_data = np.asarray(yellow_data, dtype = 'int')
lower_yellow = yellow_data[0,0:3]
upper_yellow = yellow_data[1,0:3]

pink_data = np.loadtxt('Pink_Threshold_Data.dat')
pink_data = np.asarray(pink_data, dtype = 'int')
lower_pink = pink_data[0,0:3]
upper_pink = pink_data[1,0:3]

def newImage():  
    
    ret, frame = cap.read()
    
    cv2.imshow('fisheye',frame)
    obj = Defisheye(frame, dtype='linear', format=format, fov=fov, pfov=pfov)
    new_img = obj.convert()
    blur = cv2.GaussianBlur(new_img, (7,7), 0)
    cv2.imshow('defisheye',new_img)
    return blur

def colourDetect(img, min_hsv, max_hsv):
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, min_hsv, max_hsv)
    result = cv2.bitwise_and(img,img,mask=mask)
    area = np.round(np.count_nonzero(mask) / 230400 * 100)
    return result, area

cap = cv2.VideoCapture(0)
while(True):

    frame = newImage()
    green_img, green_area = colourDetect(frame, lower_green, upper_green)
    yellow_img, yellow_area = colourDetect(frame, lower_yellow, upper_yellow)
    pink_img, pink_area = colourDetect(frame, lower_pink, upper_pink)
    cv2.imshow('green',green_img)
    cv2.imshow('yellow',yellow_img)
    cv2.imshow('pink',pink_img)
    print("Green: ", green_area, " Yellow: ", yellow_area, " Pink: ", pink_area)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # cv2.imwrite('picture.jpg',frame)
    
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
