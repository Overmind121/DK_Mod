import cv2
import numpy as np

def nothing(x):
    pass

h, s, v = 100, 100, 100
gauss = 5

cv2.namedWindow('Control Panel')  # makes a control panel
# cv.CreateTrackbar(trackbarName, windowName, initial value, range, onChange)  None
cv2.createTrackbar('hue', 'Control Panel', 30, 180, nothing)  # sets the hue trackbar on the control panel
cv2.createTrackbar('sat', 'Control Panel', 143, 255, nothing)  # sets the sat trackbar on the control panel
cv2.createTrackbar('val', 'Control Panel', 187, 255, nothing)  # sets the val trackbar on the control panel
cv2.createTrackbar('range', 'Control Panel', 89, 127, nothing)
cv2.createTrackbar('srange', 'Control Panel', 12, 127, nothing)
cv2.createTrackbar('Dilation', 'Control Panel', 13, 50, nothing)
cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    h = cv2.getTrackbarPos('hue', 'Control Panel')
    s = cv2.getTrackbarPos('sat', 'Control Panel')
    v = cv2.getTrackbarPos('val', 'Control Panel')
    r = cv2.getTrackbarPos('range', 'Control Panel')  # determines how big a slice you want from the hsv py
    sr = cv2.getTrackbarPos('srange', 'Control Panel')
    Dial = cv2.getTrackbarPos('Dilation', 'Control Panel')
    lowerthreshold = np.array([h - 10, s - sr, v - r])
    higherthreshold = np.array([h + 10, s + sr, v + r])
    mask = cv2.inRange(hsv, lowerthreshold, higherthreshold)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow("Result", result)

    edges = cv2.Canny(gray, 50, 150)
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(mask, kernel, iterations=Dial)
    cnts = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        # c is the biggest contour array
        c = max(cnts, key=cv2.contourArea)

        # calculate the radius and center of circle
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(dilation, (int(x), int(y)), int(radius), (255, 255, 0), 5, 2)


        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

    cv2.imshow('frame', frame)
    cv2.imshow('Dilations', dilation)
    cv2.imshow('edges', edges)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
cap.release()