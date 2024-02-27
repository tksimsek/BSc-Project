import json
import numpy as np
import cv2 as cv

# np.set_printoptions(threshold = np.inf)

def bound_arrays(params):
    lower_bound = np.array([params["hueLow"], params["satLow"], params["valLow"]])
    upper_bound = np.array([params["hueHigh"], params["satHigh"], params["valHigh"]])

    return lower_bound, upper_bound


with open("settings.json", "r") as read_file:
    j_data = json.load(read_file)

    lower_scooper, upper_scooper = bound_arrays(j_data["Scooper"])
    lower_tennis, upper_tennis = bound_arrays(j_data["TennisBall"])


image = cv.imread("Images/arm + ball.jpg")


def find_mids(image, bound_1, bound_2):
    # image_s = cv.resize(image, (600, 800))

    image_HSV = cv.cvtColor(image, cv.COLOR_BGR2HSV)

    mask_scooper = cv.inRange(image_HSV, bound_1[0], bound_1[1])
    mask_tennis = cv.inRange(image_HSV, bound_2[0], bound_2[1])

    indices_scooper = mask_scooper.nonzero()
    indices_tennis = mask_tennis.nonzero()

    mid_point_scooper = (int(indices_scooper[0].mean()) , int(indices_scooper[1].mean()))
    mid_point_tennis = (int(indices_tennis[0].mean()) , int(indices_tennis[1].mean()))

    # x_diff, y_diff = ((mid_point_scooper[0] - mid_point_tennis[0]), (mid_point_scooper[1] - mid_point_tennis[1]))

    # print(mid_point_scooper)
    # print(mid_point_tennis)

    # print("X diff:", x_diff)
    # print("Y diff:", y_diff)

    return mid_point_scooper, mid_point_tennis



"""
# TODO
To Normalize camera scale, measure top side area of the scooper and equal it to the pixel count (length of scooper mask indices array lenght)
"""



# print(type(mask_scooper))
# print(np.info(mask_scooper))
# print(mask_scooper[0][0])
# print(np.unique(mask_scooper)) # [  0 255]


# cv.imshow("1", mask_scooper)
# cv.imshow("2", mask_tennis)
# cv.moveWindow("2", 600, 0)

# cv.waitKey(0)
# cv.destroyAllWindows()


# Creates colored image by masking the original
# window_scooper = cv.bitwise_and(frame, frame, mask = mask_scooper)
# window_tennis = cv.bitwise_and(frame, frame, mask = mask_tennis)
