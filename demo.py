import json
import numpy as np
import cv2 as cv

from image_rec import bound_arrays, find_mids


cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FPS, 30)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))

if not cap.isOpened():
    print("Cannot open camera")
    exit()


with open("settings.json", "r") as read_file:
    j_data = json.load(read_file)

    bounds_scooper = bound_arrays(j_data["Scooper"])
    bounds_tennis = bound_arrays(j_data["RedBall"])


loop = True
while(loop):
    command = input("Press E to execute, Q to exit: ")

    if(command == "Q"):
        loop = False
        pass
    elif(command == "E"):
        ret, frame = cap.read()
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame, dropping ...")
            continue

        frame = frame[:, 150:-20] # Cropping from the sides. Adjust according to installation

        mid_scooper, mid_tennis = find_mids(frame, bounds_scooper, bounds_tennis)

        y_diff, x_diff = (mid_scooper[0] - mid_tennis[0]), (mid_scooper[1] - mid_tennis[1])

        print("X Diff: ", x_diff)
        print("Y Diff: ", y_diff)

        cv.line(frame, (mid_scooper[1], mid_scooper[0]), (mid_tennis[1], mid_tennis[0]), (0, 255, 0), thickness=3, lineType=8)
        cv.imshow('Frame', frame)
        cv.waitKey(0)
        cv.destroyWindow('Frame')

    else:
        print("Invalid option")

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()