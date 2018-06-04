import cv2
from image import ImagePr
from matplotlib import pyplot as plt
import numpy as np
# from scipy import ndimage
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

# cria uma imagem
img = ImagePr(img_path, kernel, stride)

# convolução do scipy
# convolved = ndimage.convolve(img._img, kernel, mode="constant", cval=0.0)

def plot_img(subplot, img):
    plt.subplot(subplot)
    plt.axis("off")
    plt.imshow(img)


plot_img(221, img.src)
plot_img(222, img.rgb_convolved)

plt.show()

# salva a imagem
file_name = "results/convolution_" + filter_name.split(".")[0] + "_" + img_path
img.save(file_name)
