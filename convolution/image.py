import cv2 as cv
import numpy as np

class ImagePr:
    """
    Objeto para representar uma imagem.
    Responsável por abrir, (pré)processar e salvar uma imagem.
    """

    def __init__(self, img_path, kernel, stride=1):
        self._img = cv.imread(img_path)
        # imagem redimensionada e "preenchida"
        self._preproc()

        self.shape = self._img.shape

        self._kernel = kernel
        self._k_size = len(kernel)
        self._stride = stride

        self._gray_convolved = None
        self._rgb_convolved = None

    # configura os getters para alguns atributos
    @property
    def src(self):
        return self._img[:, :, ::-1]

    @property
    def gray_convolved(self):
        if not self._gray_convolved:
            self._gray_convolved = self.gray_convolution()

        return self._gray_convolved

    @property
    def rgb_convolved(self):
        if not self._rgb_convolved:
            self._rgb_convolved = self.rgb_convolution()

        return self._rgb_convolved

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

    # def _convolve_sub(self, sub_mtrx):
    #     """
    #     aplica a convolução em uma submatriz com o mesmo tamanho do kernel
    #     """
    #     # convolução com imagem em tons de cinza
    #     element = 0
    #     # convolução com BGR
    #     # b = g = r = 0
    #
    #     for i in range(len(sub_mtrx)):
    #         for j in range(len(sub_mtrx[0])):
    #             element += sub_mtrx[i][j] * self._kernel[i][j]
    #             # b += sub_mtrx[i][j][0] * self._kernel[i][j][0]
    #             # g += sub_mtrx[i][j][1] * self._kernel[i][j][1]
    #             # r += sub_mtrx[i][j][2] * self._kernel[i][j][2]
    #
    #     return element
    #     # return (b, g, r)

    def gray_convolution(self):
        """
        aplica a convolução na imagem em tons de cinza
        """
        gray_img = cv.cvtColor(self._img, cv.COLOR_BGR2GRAY)
        convolved = []
        # percorre cada pixel da imagem
        for i in range(0, self.shape[0] - self._k_size, self._stride):
            convolved.append([])
            for j in range(0, self.shape[1] - self._k_size, self._stride):
                # jeito fácil:
                convolved[i].append((self._kernel * gray_img[i:i+self._k_size,
                                                           j:j+self._k_size]).sum())
                # jeito nem tão fácil
                # convolved[i, j] = self._convolve_sub(gray_img[i:i+self._k_size, j:j+self._k_size])

        return np.array(convolved, dtype=np.uint8)

    def rgb_convolution(self):
        """
        aplica a convolução na imagem com os tres canais: r, g, b
        """
        convolved = []
        # convolved = np.zeros(self.shape)
        # convolved = self.src
        # percorre cada pixel da imagem
        for i in range(0, self.shape[0] - self._k_size, self._stride):
            convolved.append([])
            for j in range(0, self.shape[1] - self._k_size, self._stride):
                convolved.append([
                    sum(self._kernel * self.src[i:i+self._k_size, j:j+self._k_size, 0]),
                    sum(self._kernel * self.src[i:i+self._k_size, j:j+self._k_size, 1]),
                    sum(self._kernel * self.src[i:i+self._k_size, j:j+self._k_size, 2])
                ])
                # # r
                # convolved[i, j, 0] = (self._kernel * self._img[i:i+self._k_size,
                #                                                j:j+self._k_size, 2]).sum()
                #
                # # g
                # convolved[i, j, 1] = (self._kernel * self._img[i:i+self._k_size,
                #                                                j:j+self._k_size, 1]).sum()
                #
                # # b
                # convolved[i, j, 2] = (self._kernel * self._img[i:i+self._k_size,
                #                                                j:j+self._k_size, 0]).sum()

        return np.array(convolved, dtype=np.uint8)

    def save(self, path):
        """
        salva a imagem no caminho especificado
        """
        cv.imwrite(path, self._img)
