# Most basic script to experiment with arm coordinates

from arm_control import controller

try:
    arm = controller()
    while True:
        x, y, z = input("target: ").split(",")
        arm.move(x, y, z)
except KeyboardInterrupt:
    arm.exit()
    pass