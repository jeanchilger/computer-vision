import cv2 as cv
import numpy as np

# Leitura das Imagens
src = cv.imread("input/airplane.jpg")
dst = cv.imread("input/sky.jpg")

# Criando a mascara do obejeto
mask = np.zeros(src.shape, src.dtype)
poly = np.array([[4, 80], [30, 54], [151, 63], [298, 90], [272, 134], [43, 122]], np.int32)
cv.fillPoly(mask, [poly], (255, 255, 255))

# Definindo local do objeto
width, height, _ = dst.shape
place = (500, 100)

# Clone seamlessly.
output_normal = cv.seamlessClone(src, dst, mask, place, cv.NORMAL_CLONE)
output_mixed = cv.seamlessClone(src, dst, mask, place, cv.MIXED_CLONE)
output_monochrome_transfer = cv.seamlessClone(src, dst, mask, place, cv.MONOCHROME_TRANSFER)

# Mostar os resultados
resize = lambda img: cv.resize(img, (int(img.shape[1] / 2), int(img.shape[0] / 2)))

cv.imshow("Original", resize(dst))
cv.imshow("Sobreposta", resize(src))
cv.imshow("SEAMLESS NORMAL_CLONE", resize(output_normal))
cv.imshow("SEAMLESS MIXED_CLONE", resize(output_mixed))
cv.imshow("SEAMLESS MONOCHROME_CLONE", resize(output_monochrome_transfer))

cv.waitKey(0)
cv.destroyAllWindows()
