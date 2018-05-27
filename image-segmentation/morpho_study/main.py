import cv2
from matplotlib import pyplot
import numpy as np
import sys

sys.path.insert(0, "../")
from utiltools import plot_img

# recebe o caminho da imagem por meio do terminal
img_path = sys.argv[1]
