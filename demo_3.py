import time
import json
import numpy as np
import cv2 as cv
import serial
from utils import find_port

from image_rec import bound_arrays, find_mids
from arm_control import controller


# Variables for device locations
servo_position = 0 
carrier_position = 0

arm_x = 140
arm_y = 0
arm_z = 50


# Arm controller instance
arm = controller()

# Discover and connect to driver
driver_port = find_port("driver")
if driver_port == "Device not found":
    exit(-1)

driver = serial.Serial(port=driver_port, baudrate=9600, timeout=None)
mssg = driver.readline().decode("utf-8")
if(mssg == "driver_on\n"):
    print("Serial communication established")
else:
    print(mssg)
    print("Driver out of sync")
    exit(-2)


# Start camera stream
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FPS, 30)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))
if not cap.isOpened():
    print("Cannot open the camera")
    exit(-3)


# Import image recognition parameters
with open("settings.json", "r") as read_file:
    j_data = json.load(read_file)

    bounds_scooper = bound_arrays(j_data["Scooper"])
    bounds_ball = bound_arrays(j_data["RedBall"])


# Wait for carrier to home
mssg = driver.readline().decode("utf-8")
if(mssg == "home\n"):
    print("Carrier is home")
    loop = True
else:
     print(mssg)
     print("Couldn't home the carrier")
     loop = False


for i in range(1):

    servo_position = 0
    driver.write(bytes(f"1,{servo_position}\n", 'utf-8'))

    # Incremental approach in 4 steps
    # for i in range(4):
    #     ret, frame = cap.read()
    #     ret, frame = cap.read()
    #     if not ret:
    #         print("Can't receive frame, dropping ...")
    #         continue

    #     frame = frame[:, 150:-20] # Cropping from the sides. Adjust according to installation

    #     mid_scooper, mid_ball = find_mids(frame, bounds_scooper, bounds_ball)

    #     y_diff, x_diff = (mid_scooper[0] - mid_ball[0]), (mid_scooper[1] - mid_ball[1]) # Flipped x y according to image to match the arm

    #     print("X Diff: ", x_diff)
    #     print("Y Diff: ", y_diff)

    #     # Arm target values
    #     x_target = arm_x + (x_diff / 4) - (60 / (i + 1))
    #     y_target = arm_y + (y_diff / 4)
    #     z_target = 60
    
    #     if(arm_y >= 160):
    #         z_target = -30
    #     else:
    #         print("Scooper will collide with the rails, ignoring instruction")
    #         continue

    #     arm.move(x_target, y_target, z_target)

    #     arm_x = x_target
    #     arm_y = y_target
    #     arm_z = z_target

    #     # Can come up w an equation to determine better servo angles according to x,y targets
    #     arm.set_servo(25)
    

    ret, frame = cap.read()
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame, dropping ...")
        continue

    frame = frame[:, 150:-20] # Cropping from the sides. Adjust according to installation

    mid_scooper, mid_ball = find_mids(frame, bounds_scooper, bounds_ball)

    y_diff, x_diff = (mid_scooper[0] - mid_ball[0]), (mid_scooper[1] - mid_ball[1]) # Flipped x y according to image to match the arm

    print("X Diff: ", x_diff)
    print("Y Diff: ", y_diff)

    # Arm target values
    x_target = arm_x + y_diff
    y_target = arm_y + x_diff + 30
    z_target = 40

    arm.move(x_target, y_target, z_target)
    arm.set_servo(25)

    arm_x = x_target
    arm_y = y_target
    arm_z = z_target
    
    if(arm_y >= 160):
        z_target = -50
        arm.move(x_target, y_target, z_target)
    else:
        print("Scooper will collide with the rails, ignoring instruction")
        continue
    

    # Pushing the ball on level surface
    carrier_position = 12000
    driver.write(bytes(f"2,{carrier_position}\n", 'utf-8'))

    mssg = driver.readline().decode("utf-8")
    while mssg != "moved_c\n":
        print("correct mssg not received")
        print(mssg)
        mssg = driver.readline().decode("utf-8")
        
    if(mssg == "moved_c\n"):
        print("moved carrier to: ", carrier_position)
    else:
        print("couldn't move to: ", carrier_position)
        continue

    # Arm pushing up the slope
    for i in range(100):
        arm_x += 3
        arm_z += 2
        arm.move(arm_x, arm_y, arm_z)
    

    # Arm going back
    carrier_position = 0
    driver.write(bytes(f"2,{carrier_position}\n", 'utf-8'))

    mssg = driver.readline().decode("utf-8")
    while mssg != "moved_c\n":
        print("correct mssg not received")
        print(mssg)
        mssg = driver.readline().decode("utf-8")

    if(mssg == "moved_c\n"): {
        print("moved carrier to: ", carrier_position)
    }
    else:
        print("couldn't move to: ", carrier_position)
        continue
    
    arm.reset()

    servo_position = 50
    driver.write(bytes(f"1,{servo_position}\n", 'utf-8'))

    time.sleep(1)


arm.reset()

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()