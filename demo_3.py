import time
import json
import numpy as np
import cv2 as cv
import serial
from utils import find_port

from image_rec import bound_arrays, find_mids
from arm_control import controller


# Variables for device locations
servo_position = 0      # Servo for pushback mechanism 
carrier_position = 0

arm_x = 140
arm_y = 0
arm_z = 50
arm_servo = int(10)

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
    bounds_ball = bound_arrays(j_data["TennisBall"])


# Wait for carrier to home
mssg = driver.readline().decode("utf-8")
if(mssg == "home\n"):
    print("Carrier is home")
    loop = True
else:
     print(mssg)
     print("Couldn't home the carrier")
     loop = False


for i in range(2):

    servo_position = 0
    driver.write(bytes(f"1,{servo_position}\n", 'utf-8'))

    """The camera or openCV probably buffers a frame for retrieval, 
    thats why when we actually request a frame, we receive an old one.
    To solve this we drop a frame to get the most current one."""
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
    # if (arm_x + y_diff >= 50):
    #     x_target = arm_x + y_diff - 50
    # else:
    #     x_target = arm_x + y_diff

    x_target = 10
    y_target = arm_y + x_diff + 30
    z_target = 40

    arm.move(x_target, y_target, z_target)
    arm_servo = 10
    arm.set_servo(arm_servo)

    arm_x = x_target
    arm_y = y_target
    arm_z = z_target
    
    if(arm_y >= 160):
        z_target = -50
        arm.move(x_target, y_target, z_target)
        arm_z = z_target
    else:
        print("Scooper will collide with the rails, ignoring instruction")
        continue
    

    # Pushing the ball on level surface
    carrier_position = 33000
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
    for i in range(60):
        arm_x += 3
        arm_z += 2
        arm.move(arm_x, arm_y, arm_z)

        if(i % 5 == 0):
            arm_servo += 2
            arm.set_servo(arm_servo)
        
        if(arm_y < 250):
            arm_y += 2
        elif(arm_y > 250):
            arm_y -= 2
    

    # Arm is at max X range but there is still a bit more to go
    for i in range(16):
        
        arm_z += 5
        arm.move(arm_x, arm_y, arm_z)

        if(i % 5 == 0):
            arm_servo += 2
            arm.set_servo(arm_servo)
        
        # TODO Take the following inside a function if it works
        carrier_position += 1200
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

    

    # Pulling away the Arm
    arm_x = 150
    arm.move(arm_x, arm_y, arm_z)
    arm_y = 0
    arm.move(arm_x, arm_y, arm_z)
    arm_z = 80
    arm.move(arm_x, arm_y, arm_z)
    arm_servo = 90
    arm.set_servo(arm_servo)
    

    # Carrier going back
    carrier_position = 0
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
    
    arm.reset()

    servo_position = 50
    driver.write(bytes(f"1,{servo_position}\n", 'utf-8'))
    time.sleep(1)
    servo_position = 0
    driver.write(bytes(f"1,{servo_position}\n", 'utf-8'))

    time.sleep(20)



# When everything done, release the capture and the arm
cap.release()
cv.destroyAllWindows()

arm.exit()