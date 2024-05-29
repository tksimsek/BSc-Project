from multiprocessing.connection import wait
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from utils import find_port
from uarm.wrapper import SwiftAPI


class controller():

    def __init__(self):

        com_port = find_port("arm")
        if com_port == "Device not found":
            return -1
        
        print("Arm port: ", com_port)
        self.swift = SwiftAPI(port=com_port) #, filters={'hwid': 'USB VID:PID=2341:0042'}

        self.swift.waiting_ready(timeout=3)

        device_info = self.swift.get_device_info()
        print(device_info)
        firmware_version = device_info['firmware_version']
        if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
            self.swift.set_speed_factor(0.0005)

        self.swift.set_mode(0)
        self.swift.reset(x=140, y=0, z=50, wait=True, speed=10000)


    def move_left(self):
        self.swift.set_position(x=200, y=160, z=50, wait=True)


    def move_right(self):
        self.swift.set_position(x=30, y=-200, wait=True)


    def move(self, x_target, y_target, z_target=50, speed=10000):
        self.swift.set_position(x=int(x_target), y=int(y_target), z=int(z_target), wait=True)


    def set_servo(self, degree):
        self.swift.set_wrist(int(degree))
    

    def reset(self):
        self.swift.set_position(z=200, wait=True)
        self.swift.set_position(x=140, y=0, z=80, wait=True)
    

    def exit(self):
        self.reset()
        print("Closing connection to uArm")
        self.swift.disconnect()
