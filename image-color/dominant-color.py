# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
import sys

path = sys.argv[1]
# carrega a imagem e a converte para HSV
image = np.array(cv.imread(path))
hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

# array contendo os intervalos HSV de algumas cores
COLORS = np.array([[[0,100,100], [12,255,255]], # vermelho
                   [[13,100,100], [23,255,255]], # laranjado
                   [[24,100,100], [35,255,255]], # amarelo
                   [[36,100,100], [80,255,255]], # verde
                   [[81,100,100], [92,255,255]], # ciano
                   [[93,100,100], [130,255,255]], # azul
                   [[131,100,100], [143,255,255]], # roxo
                   [[144,100,100], [170,255,255]], # magenta
                   [[0,0,0], [180,30,30]], # preto
                   [[0,0,31], [180,30,243]], # cinza
                   [[0,0,244], [180,15,255]]], np.uint8) # branco

# nomes das cores correspondendo com o indice do array
# de intervalos
COLOR_NAMES = ["Vermelho", "Laranjado", "Amarelo",
               "Verde", "Ciano", "Azul", "Roxo",
               "Magenta", "Preto", "Cinza", "Branco"]

# array para armazenar a ocorrência de cada cor
color_occurrence = np.zeros(len(COLORS), np.uint32)
color_percent = np.zeros(len(COLORS), np.uint32)
biggest_color = -1

# itera sobre cada cor para que sejam analizadas uma a uma
for i in range(len(COLORS)):

    # verifica a imagem com base nos intervalos ja definidos, retornando
    # uma mascara onde a parte branca indica a ocorrência da cor predeterminada
    mask = cv.inRange(hsv_image, COLORS[i][0], COLORS[i][1])
    # soma o "tamanho" da mascara ao array de ocorrências
    color_occurrence[i] += np.count_nonzero(mask)

    '''
    cv.imshow("Máscara: {}".format(COLOR_NAMES[i]), mask)
    cv.waitKey(0)
    cv.destroyAllWindows()
    '''


total_colors = np.sum(color_occurrence)

# calcula o percentual aproximado de ocorrência de cada cor
for i in range(len(color_occurrence)):
    color_percent[i] = (color_occurrence[i] * 100.0 / total_colors)

# matriz para representar a "paleta de cores" da imagem
rect = np.full((25,300,3), -70)

# varivel para armazenar a "posição" de inserção de valores nas colunas da matriz
it = 0

# constrói a matriz para representar a paleta de cores
for p in range(len(color_percent)):
    # 25 linhas
    for i in range(25):
        # as linhas são construidas com base na porcentagem das cores
        for j in range(color_percent[p]*3):

            rect[i][j+it] = COLORS[p][1]

    it += color_percent[p]*3

# converte a matriz para o formato uint8 que para que possa ser convertida em RGB
res_hsv = np.uint8(rect)
res = cv.cvtColor(res_hsv, cv.COLOR_HSV2BGR)
# converte a imagem original de BGR para RGB
b, g, r = cv.split(image)
image = cv.merge((r, g, b))

# mostra a imagem original em uma janela separada
'''
plt.imshow(image)
plt.axis("off")
plt.show()
'''

# plota a paleta de cores
plt.subplot(818)
plt.imshow(res)
plt.axis("off")

# plota a imagem original
plt.subplot(221)
plt.imshow(image)
plt.axis("off")

plt.subplot(222)
# posição do texto no eixo y
y_pos = 1
# decremento, com base no total de valores a serem mostrados
decrement = 1.0/11

for c in range(len(color_percent)):
    plt.text(0, y_pos, "{}: {} %".format(COLOR_NAMES[c], color_percent[c]))
    y_pos -= decrement

plt.axis("off")

# mostra tudo
plt.show()
