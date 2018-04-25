import numpy
import matplotlib.pyplot as plt
import cv2 as cv

img = numpy.zeros((550, 550, 3), numpy.uint8)
img = cv.imread("img1.jpg")
img = img[:, :, ::-1]

# img[:, :, 2] = 0  # pixels vermelhos "desativados"
# img[:, :, 1] = 0  # pixels verdes "desativados"
# img[:, :, 0] = 0  # pixels azuis "desativados"
# img = img[:, :, ::-1]  #  inversao das cores


# def get_mouse_pos(event, x, y, flags, param):
#     if event == cv.EVENT_LBUTTONDOWN:
#         print x, y


rect1 = img[205:215, 333:307]
# print img[0:20]
#img[100:150, 200:250] = rect1

cv.imshow("image", img)
# plt.imshow(img)
#cv.setMouseCallback("image", get_mouse_pos)

# plt.show()
cv.waitKey(0)
