from multiprocessing.connection import wait
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

import time
from uarm.wrapper import SwiftAPI


class controller():

    def __init__(self):
        self.swift = SwiftAPI(port="COM5", filters={'hwid': 'USB VID:PID=2341:0042'})

        self.swift.waiting_ready(timeout=3)

        device_info = self.swift.get_device_info()
        print(device_info)
        firmware_version = device_info['firmware_version']
        if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
            self.swift.set_speed_factor(0.0005)

        self.swift.set_mode(0)
        self.swift.reset(wait=True, speed=30000)


    def move_left(self):
        self.swift.set_position(x=200, y=160, z=50, wait=True)


    def move_right(self):
        self.swift.set_position(x=30, y=-200, wait=True)


    def set_servo(self, degree):
        self.swift.set_wrist(int(degree))
    

    def exit(self):
        #self.swift.reset(wait=True, speed=30000)
        self.swift.set_position(x=140, y=0, z=50, wait=True)
        # self.swift.flush_cmd(wait_stop=True)

        print("Bye")
        self.swift.disconnect()
