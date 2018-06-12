import cv2 as cv
import numpy as np

class ImagePr:
    """
    Objeto para representar uma imagem.
    Responsável por abrir, (pré)processar e salvar uma imagem.
    """

    def __init__(self, img_path, kernel, stride, *saves):
        self._img = cv.imread(img_path)
        # imagem redimensionada e "preenchida"
        self._preproc()
        self.src_gray = cv.cvtColor(self._img, cv.COLOR_BGR2GRAY)

        self.shape = self._img.shape
        self._saves = saves

        self._kernel = kernel
        self._k_size = len(kernel)
        self._stride = stride

        self._gray_convolved = []
        self._rgb_convolved = []

    # configura os getters para alguns atributos
    @property
    def src(self):
        return self._img[:, :, ::-1]

    @property
    def gray_convolved(self):
        if len(self._gray_convolved) <= 1:
            self._gray_convolved = self.gray_convolution()

        return self._gray_convolved

    @property
    def rgb_convolved(self):
        if len(self._rgb_convolved) <= 1:
            self._rgb_convolved = self.rgb_convolution()

        return self._rgb_convolved[:, :, ::-1]

    def _preproc(self):
        self._resize()
        # self._pad()

    def _resize(self, width=400):
        """
        redimensiona a imagem
        """
        ratio = width / self._img.shape[1]
        size = (width, int(self._img.shape[0]*ratio))

        self._img = cv.resize(self._img, size, interpolation=cv.INTER_AREA)

    def _pad(self):
        """
        aplica um preenchimento na borda da imagem
        """
        padding = np.zeros((self._img.shape[0]+2,
                            self._img.shape[1]+2,
                            self._img.shape[2]), dtype=np.uint8)

        padding[1:self._img.shape[0]+1, 1:self._img.shape[1]+1] = self._img
        self._img = padding

    def convert_value(sub_mtrx):
        for i in range(len(sub_mtrx)):
            for j in range(len(i)):
                sub_mtrx[i][j] = max(0, min(255, sub_mtrx[i][j]))

        print(sub_mtrx)
        return "break"

    def gray_convolution(self):
        """
        aplica a convolução na imagem em tons de cinza
        """
        convolved = []
        index = -1

        # percorre cada pixel da imagem
        for i in range(0, self.shape[0] - self._k_size, self._stride):
            convolved.append([])
            index += 1

            for j in range(0, self.shape[1] - self._k_size, self._stride):

                convolved[index].append(max(0, min(255, (self._kernel * self.src_gray[i:i+self._k_size,
                                                                                      j:j+self._k_size]).sum())))

        return np.array(convolved, dtype=np.uint8)

    def rgb_convolution(self):
        """
        aplica a convolução na imagem com os tres canais: r, g, b
        """
        convolved = []
        index = -1

        for i in range(0, self.shape[0] - self._k_size, self._stride):
            convolved.append([])
            index += 1

            for j in range(0, self.shape[1] - self._k_size, self._stride):

                convolved[index].append([
                    max(0, min(255, ((self._kernel * self.src[i:i+self._k_size, j:j+self._k_size, 2]).sum()))),
                    max(0, min(255, ((self._kernel * self.src[i:i+self._k_size, j:j+self._k_size, 1]).sum()))),
                    max(0, min(255, ((self._kernel * self.src[i:i+self._k_size, j:j+self._k_size, 0]).sum())))
                ])


        return np.array(convolved, dtype=np.uint8)

    def save(self, path):
        """
        salva a imagem no caminho especificado
        """
        for flag in self._saves:
            cv.imwrite("results/" + flag.lower() + path, eval("self._"+ flag.lower() + "_convolved"))
