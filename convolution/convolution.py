import cv2
import numpy as np
from image import Image
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
img = Image(img_path, kernel, stride)

# convolução do scipy
# convolved = ndimage.convolve(img._img, kernel, mode="constant", cval=0.0)

cv2.imshow("Convolution Example", img.gray_convolved)
cv2.waitKey(0)
cv2.destroyAllWindows()

# salva a imagem
file_name = "results/convolution_" + filter_name.split(".")[0] + "_" + img_path
img.save(file_name)
