import numpy as np
import cv2

img = cv2.imread("img1.jpg")

out = img[:]

for i in range(len(img)):

    for j in range(len(img[0])):
        outBlue = (img[i][j][2] * 0.272) + (img[i][j][1] * 0.534) + (img[i][j][0] * 0.131)
        if outBlue > 255:
            outBlue = 255
        outGreen = (img[i][j][2] * 0.349) + (img[i][j][1] * 0.686) + (img[i][j][0] * 0.168)
        if outGreen > 255:
            outGreen = 255
        outRed = (img[i][j][2] * 0.393) + (img[i][j][1] * 0.769) + (img[i][j][0] * 0.189)
        if outRed > 255:
            outRed = 255

        out[i][j] = [outBlue, outGreen, outRed]

cv2.imshow("asd", out)
cv2.waitKey(0)
cv2.destroyAllWindows()
