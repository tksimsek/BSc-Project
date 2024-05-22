import time
import json
import numpy as np
import cv2 as cv
import serial
from utils import find_port

from image_rec import bound_arrays, find_mids
from arm_control import controller

arm = controller()

carrier_port = find_port("carrier")
if carrier_port == "Device not found":
    exit(-1)

carrier = serial.Serial(port=carrier_port, baudrate=9600, timeout=1)
"""
arduino.write(bytes(x, 'utf-8')) 
time.sleep(0.1) 
data = arduino.readline()
"""

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FPS, 30)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
if not cap.isOpened():
    print("Cannot open camera")
    exit(-2)


with open("settings.json", "r") as read_file:
    j_data = json.load(read_file)

    bounds_scooper = bound_arrays(j_data["Scooper"])
    bounds_tennis = bound_arrays(j_data["TennisBall"])


loop = True
while(loop):
    command = input("Press E to execute, Q to exit: ")

    if(command == "Q"):
        loop = False
        arm.exit
        pass
    elif(command == "E"):
        ret, frame = cap.read()
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame, dropping ...")
            continue

        frame = frame[:, 180:] # Cropping from the sides. Adjust according to installation

        mid_scooper, mid_tennis = find_mids(frame, bounds_scooper, bounds_tennis)

        y_diff, x_diff = (mid_scooper[0] - mid_tennis[0]), (mid_scooper[1] - mid_tennis[1])

        print("X Diff: ", x_diff)
        print("Y Diff: ", y_diff)

        # cv.line(frame, (mid_scooper[1], mid_scooper[0]), (mid_tennis[1], mid_tennis[0]), (0, 255, 0), thickness=3, lineType=8)
        # cv.imshow('Frame', frame)
        # cv.waitKey(0)
        # cv.destroyWindow('Frame')
        
        # Arm target values
        x_target = 100      # x_target = y_diff * 0.85
        y_target = x_diff * 0.93
        z_target = 50
        if(y_target >= 160):
            z_target = -30
        else:
            print("Scooper will collide with the rails, ignoring instruction")
            continue

        arm.move(x_target, y_target, z_target)
        arm.set_servo(25) # Come up w an equation to determine servo angle according to x,y targets
        # time.sleep(2)
        # arm.move(x_target, y_target, z_target=-10) # Z range: -20,150

        # Keep the arm at this position and move the base
        carrier.write(bytes("-1000", 'utf-8'))
        
        arm.move(x_target, y_target, 10)
        time.sleep(1)
        arm.move(x_target, y_target, 30)
        time.sleep(1)
        arm.move(x_target, y_target, 50)

        arm.reset()
        # carrier.write(bytes("1200", 'utf-8'))

    else:
        print("Invalid option")


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()