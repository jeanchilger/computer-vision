import numpy
import matplotlib.pyplot as plt
import cv2


def callback(arg):
    pass


img = numpy.zeros((512, 512, 3), numpy.uint8)
cv2.namedWindow("image")

cv2.createTrackbar("R", "image", 0, 255, callback)
cv2.createTrackbar("G", "image", 0, 255, callback)
cv2.createTrackbar("B", "image", 0, 255, callback)

while True:
    cv2.imshow("image", img)
    r = cv2.getTrackbarPos("R", "image")
    g = cv2.getTrackbarPos("G", "image")
    b = cv2.getTrackbarPos("B", "image")

    img[:] = [r, g, b]

    k = cv2.waitKey(1) & 0xFF
    if k == 27: # esc
        break

cv2.destroyAllWindows()
