import cv2
from urllib.request import urlopen
import numpy as np

class VideoImage:
    @staticmethod
    def url_to_image(url: str, readFlag: int = cv2.IMREAD_COLOR):
        resp = urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, readFlag)

        # return the image
        return image