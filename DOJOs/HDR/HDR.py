import cv2
import numpy as np
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

#Pegar os tempos de abertura de câmera
times = np.array([1/30.0, 0.25, 2.5, 15.0], dtype=np.float32)

filenames = ["img_0.033.jpg", "img_0.25.jpg", "img_2.5.jpg", "img_15.jpg"]
images = []
hdr = []

#Importando as Imagens
for filename in filenames:
    img = cv2.imread("images/{}".format(filename))
    images.append(img)

fig=plt.figure(figsize=(10, 10))
fig.canvas.set_window_title("Imagens Capturadas")
columns,rows = 2, 2
times_labels = [ "0.033", "0.25", "2.5", "15.0" ]
for i in range(1, columns*rows +1):
    img = images[i-1]
    fig.add_subplot(rows, columns, i)
    plt.axis('off')
    plt.title("Exposição de {} segundos".format(times_labels[i-1]))

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

#plt.show()

print("Alinhando a mediada do limite de bitmaps")
alignMTB = cv2.createAlignMTB()
alignMTB.process(images, images)

print("Calibrando CRF")
calibrateDevec = cv2.createCalibrateDebevec()
responseDebevec = calibrateDevec.process(images, times)
cv2.imwrite("images/hdrs.xcf", responseDebevec)

print("Unindo as  Imagens")
mergeDebevec = cv2.createMergeDebevec()
hdrDebevec = mergeDebevec.process(images, times, responseDebevec)

# Metodos de HDR
# Drago
print("Gerando HDR Drago")
tonemapDrago = cv2.createTonemapDrago(1.0, 0.7)
imgHDRDrago = tonemapDrago.process(hdrDebevec)
imgHDRDrago *= 3
imgHDRDrago *= 255

hdr.append(imgHDRDrago)
cv2.imwrite("images/imgHDR_Drago.jpg", imgHDRDrago)

# Durand
print("Gerando HDR Durand")
tonemapDurand = cv2.createTonemapDurand(1.5, 4.0, 1.0, 1, 1)
imgHDRDurand = tonemapDurand.process(hdrDebevec)
imgHDRDurand *= 3
imgHDRDurand *= 255

hdr.append(imgHDRDurand)
cv2.imwrite("images/imgHDR_Durand.jpg", imgHDRDurand)

# Reinhard
print("Gerando HDR Reinhard")
tonemapReinhard = cv2.createTonemapReinhard(1.5, 0, 0, 0)
imgHDRReinhard = tonemapReinhard.process(hdrDebevec)
imgHDRReinhard *= 255

hdr.append(imgHDRReinhard)
cv2.imwrite("images/imgHDR_Reinhard.jpg", imgHDRReinhard)

# Mantiuk
print("Gerando HDR Mantiuk")
tonemapMantiuk = cv2.createTonemapMantiuk(2.2, 0.85, 1.2)
imgHDRMantiuk = tonemapMantiuk.process(hdrDebevec)
imgHDRMantiuk *= 3
imgHDRMantiuk *= 255

hdr.append(imgHDRMantiuk)
cv2.imwrite("images/imgHDR_Mantiuk.jpg", imgHDRMantiuk)

# Resultados Finais
print("Gerando resultados Finais")
fig=plt.figure(figsize=(10, 10))
fig.canvas.set_window_title("Resultado da aplicação de HDR")
columns,rows = 2, 2
hdr_method = ["Draco","Durand","Reinhard","Matiuk"]
for i in range(1, columns*rows +1):
    img = hdr[i-1]
    fig.add_subplot(rows, columns, i)
    plt.axis('off')
    plt.title(hdr_method[i-1])

    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB).astype(np.uint8))

plt.show()
