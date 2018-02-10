import cv2
import numpy as np

from pipeline.processor.Processor import Processor


class Rotate(Processor):
    def __init__(self, angle_func, *args, **kwargs):
        self.angle_func = angle_func
        
    def iterate(self):
        t = 0
        for frame in self.source:
            w, h = self.resolution
            t = (t + 1 / self.framerate)
            M = cv2.getRotationMatrix2D((w // 2, h // 2), self.angle_func(t), 1.)
            yield cv2.warpAffine(
                frame, M,
                (frame.shape[1], frame.shape[0]),
                borderMode=cv2.BORDER_CONSTANT,
                borderValue=(100, 100, 100)
            )
