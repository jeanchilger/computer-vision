import cv2
from image import ImagePr
from matplotlib import pyplot as plt
import numpy as np
import sys

# pega os parametros passados por meio do terminal
img_path = sys.argv[1]
filter_name = sys.argv[2]
stride = int(sys.argv[3])

# le o arquivo contendo o filtro e o transforma em uma matriz
with open(filter_name, "r") as filter_file:
    list_ = filter_file.read().splitlines()
    kernel = []

    for line in list_:
        kernel.append(line.split(" "))

kernel = np.array(kernel, dtype=np.float_)

# cria uma imagem para ser processada
img = ImagePr(img_path, kernel, stride, "Gray", "RGB")

def plot_img(subplot, img, cmapping=None, txt=None):
    # configura o espaçamento dos subplots
    plt.subplots_adjust(bottom=0, top=.97, left=0, right=1, wspace=.07, hspace=.07)
    plt.subplot(subplot)
    plt.axis("off")
    plt.imshow(img, cmap=cmapping)
    plt.text(1, -9, txt)


plot_img(221, img.src, txt="Imagem RGB")
plot_img(222, img.rgb_convolved, txt="Filtro RGB")
plot_img(223, img.src_gray, "gray", "Imagem Cinza")
plot_img(224, img.gray_convolved, "gray", "Filtro Cinza")

plt.show()

# salva a imagem
file_name = "/convolution_" + filter_name.split(".")[0] + "_" + img_path
img.save(file_name)
