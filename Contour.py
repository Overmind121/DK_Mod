#from collections import deque
import numpy as np  # math libraries
#import argparse  # to find and pass files
import imutils  # resizing
import cv2  # opencv itself
from PIL import ImageGrab  # for screen capture
#from matplotlib import pyplot as plt


def nothing(x):
    pass

# Callback Function for Trackbar (but do not any work)
# def trackCircle(mask):
#     cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
#     if len(cnts)>0:
#         c = max(cnts, key = cv2.ContourArea)
#         ((x,y), radius) = cv2.minEnclosingCircle(c)
#         cv2.circle(frame, (int(x), int(y), 0, 255, 255, 2))



from collections import deque
h, s, v = 100, 100, 100
gauss = 5
# sets the global variables for the hue, sat, and val


cv2.namedWindow('Control Panel')  # makes a control panel
# cv.CreateTrackbar(trackbarName, windowName, initial value, range, onChange)  None
cv2.createTrackbar('hue', 'Control Panel', 0, 180, nothing)  # sets the hue trackbar on the control panel
cv2.createTrackbar('sat', 'Control Panel', 205, 255, nothing)  # sets the sat trackbar on the control panel
cv2.createTrackbar('val', 'Control Panel', 255, 255, nothing)  # sets the val trackbar on the control panel
cv2.createTrackbar('range', 'Control Panel', 69, 127, nothing)
cv2.createTrackbar('srange', 'Control Panel', 25, 127, nothing)
device = cv2.VideoCapture(0)

while True:
    _, frame = device.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    h = cv2.getTrackbarPos('hue', 'Control Panel')
    s = cv2.getTrackbarPos('sat', 'Control Panel')
    v = cv2.getTrackbarPos('val', 'Control Panel')
    r = cv2.getTrackbarPos('range', 'Control Panel') #determines how big a slice you want from the hsv py
    sr = cv2.getTrackbarPos('srange', 'Control Panel')

    lowerthreshold = np.array([h-10, s-sr, v-r])
    higherthreshold = np.array([h+10, s+sr, v+r])

    mask = cv2.inRange(hsv, lowerthreshold, higherthreshold)
    #mask = cv2.GaussianBlur(mask,(5,5), gauss)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]

    #if cnts point list is non empty
    if len(cnts)>0:
        #c is the biggest contour array
        c = max(cnts, key = cv2.contourArea)

        #calculate the radius and center of circle
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(frame, (int(x), int(y)), int(radius),( 255, 255,0),5, 2)
        #cv2.circle(mask, (int(x), int(y)), int(radius), color[, thickness[, lineType[, shift]]])

    cv2.imshow("frame",frame)
    cv2.imshow("mask", mask)
    #track = cv2.bitwise_and(frame,frame,mask=final)
    #cv2.imshow("Tracking", track)
    #bitwise function to implement the mask on the frame 
    result = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow("Result", result)

    if cv2.waitKey(1) == 27:
        break

device.release()
cv2.destroyAllWindows()