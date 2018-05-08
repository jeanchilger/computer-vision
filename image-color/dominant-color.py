import numpy as np
import cv2 as cv
import sys
from matplotlib import pyplot as plt

# array contendo os intervalos HSV de algumas cores
COLORS = np.array([[[0,100,100], [7,255,255]], # vermelho
                   [[8,100,100], [22,255,255]], # laranjado
                   [[23,100,100], [35,255,255]], # amarelo
                   [[36,100,100], [80,255,255]], # verde
                   [[81,100,100], [92,255,255]], # ciano
                   [[93,100,100], [130,255,255]], # azul
                   [[131,100,100], [143,255,255]], # roxo
                   [[144,100,100], [170,255,255]], # magenta
                   [[0,0,0], [180,30,30]], # preto
                   [[0,0,31], [180,30,233]], # cinza
                   [[0,0,234], [180,15,255]]], # branco
                   np.uint8)

# cores para mostrar na paleta
COLORS_OUT = np.array([[0,255,255], # vermelho
                       [10,255,250], # laranjado
                       [27,255,240], # amarelo
                       [60,255,200], # verde
                       [85,255,225], # ciano
                       [121,255,250], # azul
                       [138,255,255], # roxo
                       [155,255,250], # magenta
                       [0,0,0], # preto
                       [0,0,85], # cinza
                       [0,0,255]], # branco
                       np.uint8)

# nomes das cores correspondendo com o indice do array
# de intervalos
COLOR_NAMES = ["Vermelho", "Laranjado", "Amarelo",
               "Verde", "Ciano", "Azul", "Roxo",
               "Magenta", "Preto", "Cinza", "Branco"]


# objeto para representar a imagem
class Image:

    def __init__(self, path):

        # carrega a imagem
        self.__src = np.array(cv.imread(path))
        # converte a imagem para HSV
        self.hsv_image = cv.cvtColor(self.__src, cv.COLOR_BGR2HSV)
        # converte a imagem para RGB
        self.rgb_image = cv.cvtColor(self.hsv_image, cv.COLOR_HSV2RGB)

        # arrays para armazenar a frequência das cores (absoluta e relativa)
        self.color_occurrence = np.zeros(len(COLORS), np.uint32)
        self.color_percentage = np.zeros(len(COLORS), np.uint32)

        self._calculate_occurrence()
        self._calculate_percentage()

    # calcula a ocorrência de cada cor
    def _calculate_occurrence(self):

        # verifica cada uma das cores
        for i in range(len(COLORS)):

            # verifica a imagem com base nos intervalos de cores definidos e retorna uma máscara
            # a parte branca da máscara indica a presença da cor verificada
            mask = cv.inRange(self.hsv_image, COLORS[i][0], COLORS[i][1])

            # soma o "tamanho" da mascara ao array de ocorrências
            self.color_occurrence[i] += np.count_nonzero(mask)

            # exemplo de mascara
            '''
            cv.imshow("Máscara: {}".format(COLOR_NAMES[i]), mask)
            cv.waitKey(0)
            cv.destroyAllWindows()
            '''

    # calcula o percentual aproximado de ocorrência de cada cor
    def _calculate_percentage(self):
        # pega o numero de ocorrencias para calcular o percentual
        total_colors = np.sum(self.color_occurrence)

        for i in range(len(self.color_occurrence)):
            self.color_percentage[i] = round((self.color_occurrence[i] * 100.0 / total_colors))

def create_palette(percentage_array):
    # matriz para representar a "paleta de cores" da imagem
    rect = np.full((25,300,3), 70)

    # variavel para armazenar a "posicao" das colunas da matriz
    it = 0

    # constroi a matriz para representar a paleta de cores
    for p in range(len(percentage_array)):

        # 25 linhas (25px de altura)
        for i in range(25):

            # as linhas são construidas com base na porcentagem das cores (100*3px de largura)
            for j in range(percentage_array[p]*3):

                # adiciona uma cor a um pixel
                rect[i][j+it] = COLORS_OUT[p]

        # local (da coluna) por onde começar o próximo loop
        it += percentage_array[p]*3

    # converte o retângulo criado para o formato RGB
    res_hsv = np.uint8(rect)
    res = cv.cvtColor(res_hsv, cv.COLOR_HSV2RGB)

    return res

# função para plotar imagens
def plot_img(subplot, img):
    plt.subplot(subplot)
    plt.imshow(img)
    plt.axis("off")

# função para plotar texto
def plot_txt(subplot, percentage_array):
    plt.subplot(subplot)
    # posição inicial do texto no eixo y
    y_pos = 1
    # decremento, com base no total de valores a serem mostrados
    decrement = 1.0/11

    for i in range(len(percentage_array)):
        plt.text(0, y_pos, "{}: {} %".format(COLOR_NAMES[i], percentage_array[i]))
        y_pos -= decrement

    plt.axis("off")


if __name__ == "__main__":
    # pega o nome da imagem passado como argumento pelo terminal
    path = sys.argv[1]
    # cria uma representação da imagem contida em path
    img = Image(path)
    # cria uma paleta com as cores predominantes da imagem
    palette = create_palette(img.color_percentage)

    # mostra a imagem original se outro argumento for passado
    if (len(sys.argv) > 2):
        plot_img(111, img.rgb_image)
        plt.show()

    # configura o fundo do pyplot como cinza
    plt.style.use("grayscale")
    # plotagens
    plot_img(818, palette)
    plot_img(221, img.rgb_image)
    plot_txt(222, img.color_percentage)
    plt.show()
