# coding=utf-8
import cv2
import numpy as np
import matplotlib.pyplot as plt

icon = cv2.imread("img1.png")
rows, cols, ch = icon.shape  # pega as dimensões da imagem (para fazer ROI com a imagem maior)

poly = cv2.imread("img2.jpg")

roi = poly[0:rows, 0:cols]  # ROI do tamanho do icone
img_gray = cv2.cvtColor(icon, cv2.COLOR_BGR2GRAY)  # converte o icone para a cor cinza para aplicar o threshold

ret, mask = cv2.threshold(img_gray, 75, 255, cv2.THRESH_BINARY)  # se (x,y) > 75 --> (x,y) = 255
mask_inv = cv2.bitwise_not(mask)  # inverte a mascara

poly_bg = cv2.bitwise_and(roi, roi, mask=mask) # onde a máscara é preta, poly_bg fica preto

icon_fg = cv2.bitwise_and(icon, icon, mask=mask_inv) # (bit wise and) entre icon e icon e mask altera os valores resultantes

dst = cv2.add(poly_bg, icon_fg) # soma os pixels (preto + qualquer cor == qualquer cor)

poly[0:rows, 0:cols] = dst

cv2.imshow("mask", mask)
cv2.imshow("poly_bg", poly_bg)
#cv2.imshow("icon_fg", icon_fg)
# cv2.imshow("dst", dst)


cv2.waitKey(5500)
cv2.destroyAllWindows()
exit()
