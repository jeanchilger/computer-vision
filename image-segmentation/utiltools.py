import cv2
import numpy as np
from matplotlib import pyplot

def plot_img(*content):
    # configura o espaçamento dos subplots
    pyplot.subplots_adjust(bottom=0, top=.97, left=0, right=1, wspace=.06, hspace=.06)
    # calcula a quantidade dos subplots
    plot_x = 2
    plot_y = len(content) // 2
    plot_i = 1

    for img, txt in content:
        pyplot.subplot(plot_x, plot_y, plot_i)
        plot_i += 1
        # imagem original
        try:
            ready_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        except:
            ready_img = img[:, :, ::-1]

        pyplot.axis("off")
        pyplot.imshow(ready_img)
        # plota o texto correspondente a imagem no mesmo subplot
        plot_txt(txt)

def plot_txt(txt):
    pyplot.text(1, -9, txt)
