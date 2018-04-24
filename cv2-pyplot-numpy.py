import numpy
import matplotlib.pyplot as plt
import cv2

img = numpy.zeros((600, 600, 3), numpy.uint8)
img = cv2.ellipse(img, (300, 140), (100, 100), 60, 60, 360, (255, 0, 0), -1, cv2.LINE_AA)
img = cv2.ellipse(img, (300, 140), (45, 45), 0, 0, 360, (0, 0, 0), -1, cv2.LINE_AA)

img = cv2.ellipse(img, (184, 350), (100, 100), 0, 0, 300, (0, 255, 0), -1, cv2.LINE_AA)
img = cv2.ellipse(img, (184, 350), (45, 45), 0, 0, 360, (0, 0, 0), -1, cv2.LINE_AA)

img = cv2.ellipse(img, (416, 350), (100, 100), -60, 0, 300, (0, 0, 255), -1, cv2.LINE_AA)
img = cv2.ellipse(img, (416, 350), (45, 45), 0, 0, 360, (0, 0, 0), -1, cv2.LINE_AA)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (60, 550), font, 4, (255, 255, 255), 10, cv2.LINE_AA)

plt.imshow(img)
plt.show()
