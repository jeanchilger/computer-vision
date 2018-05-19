import cv2
import numpy as np
import sys
from utiltools import *

# pega o caminho da imagem por meio de um parâmetro do terminal
img_path = sys.argv[1]
# verifica se existe um parâmetro especificando o tamanho do kernel
if len(sys.argv) == 2:
    sys.argv.append(5)

# imagem BGR sem nenhum processamento
src_img = cv2.imread(img_path)
# converte a imagem para tons de cinza
gray_img = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)

# # aplica o blur gaussiano (redução de ruído)
# suavized_img = cv2.GaussianBlur(gray_img, (7, 7), 0)
# # cv2.threshold(src, X, Y, flag) --> se o valor de um pixel for maior que X, ele será mudado para Y
# r, mask = cv2.threshold(suavized_img, 160, 255, cv2.THRESH_BINARY)


# binarização adaptativa
mask = cv2.adaptiveThreshold(gray_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                             cv2.THRESH_BINARY, 115, 1)

# relacionado à convolução
# TODO: STUDY THIS
# Acho que entendi: vai fazer a convolução e se todos os pixels no kernel forem 1, fica 1 senão, fica 0 (é isso ai)
kernel = np.ones((int(sys.argv[2]), int(sys.argv[2])), np.uint8)

# realiza a erosão da imagem
eroded_img = cv2.erode(src_img, kernel, iterations=1)

# realiza a dilatação da imagem
dilated_img = cv2.dilate(src_img, kernel, iterations=1)

# erosão seguida de uma dilatação
er_di_img = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# dilatação seguida de uma erosão
di_er_img = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

res_mtrx = [[src_img, "Original"], [mask, "Binarizada"], [eroded_img, "Erosão"],
           [dilated_img, "Dilatação"], [er_di_img, "Erosão e depois Dilatação"],
           [di_er_img, "Dilatação e depois Erosão"]]

# plot_img([src_img, "Original"], [mask, "Binarizada"], [eroded_img, "Erosão"],
#          [dilated_img, "Dilatação"], [er_di_img, "Erosão e depois Dilatação"],
#          [di_er_img, "Dilatação e depois Erosão"])
#
# pyplot.show()

for img, title in res_mtrx:
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
