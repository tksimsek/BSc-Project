import json
import serial
import numpy as np
import cv2 as cv

base_postition = 0

# https://docs.opencv.org/4.7.0/d4/d73/tutorial_py_contours_begin.html


def setup():
    setup_serial()
    # calibrate platform position
    return


def setup_serial():
    # set serial comm w arduino
    global arduino 
    arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

    """arduino.write(bytes(x, 'utf-8')) 
	   time.sleep(0.1) 
	   data = arduino.readline()
    """
    """
    messages:
    home.
    top..
    u1000
    d200.
    """
    return


def calibrate():
    return


def locate_objectives():
    # find coordinates of rock and arm end effector  
    return


def move_arm_to_objective():
    return


def move_base_to_top():
    # Lift up the arm effector 
    return


def move_base_to_bot():
    return


def main_loop():
    locate_objectives()
    move_arm_to_objective()
    move_base_to_top()
    move_base_to_bot()
    # Loop
    return


def main():
    setup()
    main_loop()


if __name__ == "__main__":
    main()