from arm_control import controller

arm = controller()

for i in range(50):
    x, y, z = input("target: ").split(",")
    arm.move(x, y, z)