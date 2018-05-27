import cv2
from matplotlib import pyplot as plt
import numpy as np
# from scipy import ndimage
import sys


# pega os parametros passados por meio do terminal
img_path = sys.argv[1]
filter_name = sys.argv[2]
stride = int(sys.argv[3])

# carrega a imagem em tons de cinza
img_gray = cv2.imread(img_path, 0)

# le o arquivo contendo o filtro e o transforma em uma matriz
with open(filter_name, "r") as filter_file:
    list_ = filter_file.read().splitlines()
    kernel = []

    for line in list_:
        kernel.append(line.split(" "))

    kernel = np.array(kernel, dtype=np.uint8)

# matriz para armazenar a imagem após o processo de convolução
convolved = []

# realiza a convolução em uma parte da imagem com as mesmas dimensões do kernel
def convolve_image(sub_mtrx):
    # element que guarda o resultado da convolução
    element = 0

    for i in range(len(sub_mtrx)):
        for j in range(len(sub_mtrx[0])):
            element += sub_mtrx[i][j] * kernel[i][j]

    return element
print (len(img_gray), len(kernel))
for i in range(0, len(img_gray) - len(kernel), stride):
    # a imagem resultante terá o mesmo número de linhas e colunas que a original
    convolved.append([])

    for j in range(0, len(img_gray[0]) - len(kernel[0]), stride):
        convolved[i].append(convolve_image(img_gray[i:i+len(kernel),
                                                    j:j+len(kernel[0])]))

convolved = np.array(convolved, dtype=np.uint8)
# convolução do scipy
# convolved = ndimage.convolve(img_gray, kernel, mode="constant", cval=0.0)

cv2.imshow("Convolution Example", convolved)
cv2.waitKey(0)
cv2.destroyAllWindows()

# prepara o nome do arquivo a ser salvo
file_name = "results/convolution_" + filter_name.split(".")[0] + "_" + img_path
# salva o arquivo
cv2.imwrite(file_name, convolved)
