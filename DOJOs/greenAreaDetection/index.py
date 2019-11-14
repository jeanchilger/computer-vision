import cv2 as cv
import numpy as np
from functools import reduce

def resize(img, ratio=2):
    return cv.resize(img, 480)


def dstretch(A, tol=None):
    orig_shape = A.shape
    A = A.reshape((-1, 3)).astype(np.float)

    cov = np.cov(A.T)
    sigma = np.diag(np.sqrt(cov.diagonal()))

    eigval, V = np.linalg.eig(cov)
    S = np.diag(1 / np.sqrt(eigval))
    mean = np.mean(A, axis=0)
    A -= mean
    T = reduce(np.dot, [sigma, V, S, V.T])

    offset = mean - np.dot(mean, T) ## mean * T == np.dot(mean, T)

    A = np.dot(A, T)
    A += mean + offset

    B = A.reshape(orig_shape)

    for channel in range(3):
        if tol:
            low, high = np.percentline(B[:, :, channel], 100 * tol), np.percentline(B[:, :, channel], 100 - 100 * tol)
            B[B < low] = low
            B[B > high] = high

        B[:, :, channel] = 255 * (B[:, :, channel] - B[:, :, channel].min()) / (B[:, :, channel].max() - B[:, :, channel].min())

    return B.astype(np.uint8)



img = cv.imread("img1.png")
#img = cv.resize(img, int(img.shape[1] / 2))

k = 3
gaussian = cv.blur(img, (k, k))

saturated = dstretch(gaussian)

saturated[:, :, 0] = 0
saturated[:, :, 2] = 0

ret, binary_img = cv.threshold(saturated, 127, 255, cv.THRESH_BINARY)

kernel = np.ones((k, k), np.uint8)
eroded = cv.erode(binary_img, kernel, iterations=1)

mask = cv.cvtColor(eroded, cv.COLOR_BGR2GRAY)
classification = cv.subtract(img, eroded)

cv.imshow("Output", classification)

cv.waitKey(0)
cv.destroyAllWindows()
