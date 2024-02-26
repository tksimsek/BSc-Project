import json
import numpy as np
import cv2 as cv


def bound_arrays(params):
    lower_bound = np.array([params["hueLow"], params["satLow"], params["valLow"]])
    upper_bound = np.array([params["hueHigh"], params["satHigh"], params["valHigh"]])

    return lower_bound, upper_bound


cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

with open("settings.json", "r") as read_file:
    j_data = json.load(read_file)

    lower_scooper, upper_scooper = bound_arrays(j_data["Scooper"])
    lower_tennis, upper_tennis = bound_arrays(j_data["TennisBall"])
    # lower_ping_pong, upper_ping_pong = bound_arrays(param_ping_pong)



while True:
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame, exiting ...")
        break

    # Create different frames here
    frameHSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    mask_scooper = cv.inRange(frameHSV, lower_scooper, upper_scooper)
    mask_tennis = cv.inRange(frameHSV, lower_scooper, upper_scooper)

    window_scooper = cv.bitwise_and(frame, frame, mask = mask_scooper)
    cv.imshow('Scooper Mask', window_scooper)
    cv.moveWindow('Scooper Mask', 750, 520)

    window_tennis = cv.bitwise_and(frame, frame, mask = mask_tennis)
    cv.imshow('Tennis Mask', window_tennis)
    cv.moveWindow('Tennis Mask', 100, 520)
    
    cv.imshow('Original', frame)
    cv.moveWindow('Original', 100, 0)


    if cv.waitKey(1) == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()


