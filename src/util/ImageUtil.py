import urllib.request
import cv2
import numpy as np


def loadImage(url):
    with urllib.request.urlopen(url) as response:
        image = np.asarray(bytearray(response.read()), dtype="uint8")
        return cv2.imdecode(image, cv2.IMREAD_COLOR)
