import json
import numpy as np
import cv2 as cv


def bound_arrays(params):
    lower_bound = np.array([params["hueLow"], params["satLow"], params["valLow"]])
    upper_bound = np.array([params["hueHigh"], params["satHigh"], params["valHigh"]])

    return lower_bound, upper_bound

with open("settings.json", "r") as read_file:
    j_data = json.load(read_file)

    lower_scooper, upper_scooper = bound_arrays(j_data["Scooper"])
    lower_tennis, upper_tennis = bound_arrays(j_data["TennisBall"])

image_1 = cv.imread("Images/arm.jpg")
image_1_s = cv.resize(image_1, (600, 800))

image_2 = cv.imread("Images/arm + ball.jpg")
image_2_s = cv.resize(image_2, (600, 800))


image_2_HSV = cv.cvtColor(image_2_s, cv.COLOR_BGR2HSV)

mask_scooper = cv.inRange(image_2_HSV, lower_scooper, upper_scooper)
mask_tennis = cv.inRange(image_2_HSV, lower_tennis, upper_tennis)


# Creates colored image by masking the original
# window_scooper = cv.bitwise_and(frame, frame, mask = mask_scooper)
# window_tennis = cv.bitwise_and(frame, frame, mask = mask_tennis)



cv.imshow("1", mask_scooper)
cv.imshow("2", mask_tennis)
cv.moveWindow("2", 600, 0)

cv.waitKey(0)
cv.destroyAllWindows()








# np.set_printoptions(threshold = np.inf)

# size = 2
# thickness = 2

# height = 10
# width = 10

# mask = np.zeros((width, height), dtype=int)
# print(mask)
# print("\n")

# for y in range(height):
#     for x in range(width):
#         if (width/2 - size) <= x < (width/2 + size):
#             if (height/2 - size) <= y < (height/2 + size):
#                 mask[x, y] = 1
        
        


# file = open("MyFile.txt", "w")
# file.truncate(0)
# content = str(mask)
# file.write(content)
# file.close()

# print(mask)

