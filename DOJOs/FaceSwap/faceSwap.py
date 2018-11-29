import numpy as np
import cv2
import functions as func

# Imagens que temos
filename1 = 'ted_cruz.jpg'
# filename1 = 'donald_trump.jpg'
# filename1 = 'hillary_clinton.jpg'
# filename1 = 'obama.jpg'

# filename2 = 'ted_cruz.jpg'
filename2 = 'donald_trump.jpg'
# filename2 = 'hillary_clinton.jpg'
# filename2 = 'obama.jpg'

# importar as imagens
print("Coletando as Imagens")
img1 = cv2.imread("images/" + filename1) # src
img2 = cv2.imread("images/" + filename2) # dst
img1Warped = np.copy(img2)

print("Coletando os pontos faciais correspondentes")
points1 = func.readPoints("points/"+filename1+".txt")
points2 = func.readPoints("points/"+filename2+".txt")

func.plot("Step1-FaceAlignment.jpg")

print("Criando os vetores das funções convexas")
hull1 = []
hull2 = []

print("Intersecção dos conjuntos das funções convexas, terminadas pelas distâncias euclidianas")
hullIndex = cv2.convexHull(np.array(points2), returnPoints=False)
for i in range(0, len(hullIndex)):
    hull1.append(points1[int(hullIndex[i])])
    hull2.append(points2[int(hullIndex[i])])

print("Triangularização de Delaunay aplicada pelos prontos faciais")
sizeImg2 = img2.shape
rect = (0, 0, sizeImg2[1], sizeImg2[0])
dt = func.calculateDelaunayTriangles(rect, hull2)
if len(dt) == 0:
    quit()

print("\tAplicando a Triangularização de Delaunay")
for i in range(0, len(dt)):
    t1 = []
    t2 = []
    # Pega os pontos correspondentes dos triangulos aos das imagens
    for j in range(0, 3):
        t1.append(hull1[dt[i][j]])
        t2.append(hull2[dt[i][j]])

    # unifica a imagem com as regiões dos triangulos das imagens
    func.warpTriangle(img1, img1Warped, t1, t2)

func.plot("Step2-SeamlessCloning.jpg")

print("Calculando e criando a Máscara")
hull8U = []
for i in range(0, len(hull2)):
    hull8U.append((hull2[i][0], hull2[i][1]))

mask = np.zeros(img2.shape, dtype=img2.dtype) # mask

print("Desenho dos poligonos convexos preenchidos")
cv2.fillConvexPoly(mask, np.int32(hull8U), (255, 255, 255))

print("Limitaçãos dos triangulos")
r = cv2.boundingRect(np.float32([hull2]))
center = (r[0] + int(r[2] / 2), r[1] + int(r[3] / 2))

print("Aplicando o Seamless Cloning")
output = cv2.seamlessClone(np.uint8(img1Warped), img2, mask, center, cv2.NORMAL_CLONE)

cv2.imshow("Face Swapped", output)
cv2.waitKey(0)
cv2.destroyAllWindows()
