import cv2
import numpy as np
from matplotlib import pyplot

def plot_img(*content):
    plot_x = len(content) // 2
    plot_y = 2
    plot_i = 1
    for img, txt in content:
        pyplot.subplot(plot_x, plot_y, plot_i)
        plot_i += 1
        try:
            ready_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        except:
            ready_img = img[:, :, ::-1]
        pyplot.axis("off")
        pyplot.imshow(ready_img)
        plot_txt(txt)

def plot_txt(txt):
    pyplot.text(1, -4, txt)
