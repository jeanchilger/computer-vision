import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while True:

    # Take each frame
    ret, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= mask)

    # cv.imshow("img", frame[:, ::-1]) # usa [:, ::-1] para ficar "simetrico"
    # cv.imshow("mask", mask)
    cv.imshow("res",res)
    k = cv.waitKey(1) & 0xFF
    if k == ord("q"):
        break

cv.destroyAllWindows()
cap.release()
