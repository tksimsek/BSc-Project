import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(cv.CAP_PROP_FPS, 30)
cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*'MJPG'))

if not cap.isOpened():
    print("Cannot open camera")
    cap.release()
    exit()


while True:
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame, exiting ...")
        break

    crop_img = frame[:, 180:]
    crop_img = cv.resize(crop_img, (600, 800))
    cv.imshow("Cropped", crop_img)
    cv.moveWindow('Cropped', 100, 0)

    if cv.waitKey(1) == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv.destroyAllWindows()