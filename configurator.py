import numpy as np
import cv2 as cv

print(cv.__version__)


def onTrack1(val):
    global hueLow
    hueLow = val
    print('Hue Low', hueLow)

def onTrack2(val):
    global hueHigh
    hueHigh = val
    print('Hue High', hueHigh)

def onTrack3(val):
    global satLow
    satLow = val
    print('Sat Low', satLow)

def onTrack4(val):
    global satHigh
    satHigh = val
    print('Sat High', satHigh)

def onTrack5(val):
    global valLow
    valLow = val
    print('Val Low', valLow)

def onTrack6(val):
    global valHigh
    valHigh = val
    print('Val High', valHigh)

width = 600
height = 800

image_2 = cv.imread("Images/arm + ball.jpg")
image_2_s = cv.resize(image_2, (width, height))

cv.namedWindow('myTracker')
cv.moveWindow('myTracker', int(width * 1.5), 0)

hueLow = 0
hueHigh = 33
satLow = 80
satHigh = 255
valLow = 110
valHigh = 255

cv.createTrackbar('Hue Low', 'myTracker', 0, 179, onTrack1)
cv.createTrackbar('Hue High', 'myTracker', 33, 179, onTrack2)
cv.createTrackbar('Sat Low', 'myTracker', 80, 255, onTrack3)
cv.createTrackbar('Sat High', 'myTracker', 255, 255, onTrack4)
cv.createTrackbar('Val Low', 'myTracker', 110, 255, onTrack5)
cv.createTrackbar('Val High', 'myTracker', 255, 255, onTrack6)

while True:
    frame = image_2_s

    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])
    myMask = cv.inRange(frameHSV, lowerBound, upperBound)

    myObject = cv.bitwise_and(frame, frame, mask = myMask)
    myObjectSmall = cv.resize(myObject, (int(width/2), int(height/2)))
    cv.imshow('My Object', myObjectSmall)
    cv.moveWindow('My Object', width, 0)

    myMaskSmall = cv.resize(myMask, (int(width/2), int(height/2)))
    cv.imshow('My Mask', myMaskSmall)
    cv.moveWindow('My Mask', width, int(height/2))

    contours, hierarchy = cv.findContours(myMask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contouredFrame = cv.drawContours(frame, contours, 0, (0,255,0), 2)
    
    cv.imshow('Original', contouredFrame)
    cv.moveWindow('Original', 0, 0)
    
    if cv.waitKey(1) & 0xff == ord('q'):
        break
