import serial.tools.list_ports

DRIVER_HWID = "USB VID:PID=2341:0058 SER=BB6F77CF51514746304B2020FF0A4054 LOCATION=1-2"
UARM_HWID = "USB VID:PID=2341:0042 SER=55739323337351706142 LOCATION=1-2"


def find_port(device=""):
    """Returns the current COM Port number for given device=("Arm" or "driver")"""

    ports = serial.tools.list_ports.comports()

    uarm_port = ""
    driver_port = ""

    for port, desc, hwid in sorted(ports):
        if "Arduino Mega 2560" in desc:
            uarm_port = str(port)
        elif "Arduino NANO Every" in desc:
            driver_port = str(port)
        else:
            continue
    
    if device.lower() == "arm":
        return uarm_port
    elif device.lower() == "driver":
        return driver_port
    else:
        return "Device not found"


# for port, desc, hwid in sorted(ports):
#     if hwid == UARM_HWID:
#         uarm_port = str(port)
#     elif hwid == DRIVER_HWID:
#         driver_port = str(port)
#     else:
#         continue