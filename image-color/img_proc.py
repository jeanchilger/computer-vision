import threading

class Preprocessor(threading.Thread):

    def __init__(self, img_segment, low_interval, high_interval):
        threading.Thread.__init__(self)
        self.image = img_segment
        self.color_occurred = []
        self.color_score = []

        # armazena o intervalo do hue (grau da cor) da cor de maior ocorrência
        self.hue_range = range(low_interval[0], high_interval[0])
        # armazena o intervalo da saturação da cor de maior ocorrência
        self.saturation_range = range(low_interval[1], high_interval[1])
        # armazena o intervalo do contraste da cor de maior ocorrência
        self.contrast_range = range(low_interval[2], high_interval[2])


    def run(self):
        for row in self.image:

            for pixel in row:

                if pixel[0] in self.hue_range:
                    if pixel[1] in self.saturation_range:
                        if pixel[2] in self.contrast_range:
                            if str(pixel) not in self.color_occurred:
                                self.color_occurred.append(str(pixel))
                                self.color_score.append(1)
                            else:
                                i = self.color_occurred.index(str(pixel))
                                self.color_score[i] += 1
        print(self.color_occurred)

if __name__ == "__main__":
    pass
