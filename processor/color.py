import random

import cv2

from pipeline.processor.Processor import Processor


class ChangeColorspace(Processor):

    def __init__(self, target_space=cv2.COLOR_BGR2GRAY):
        self.target_space = target_space

    def iterate(self):
        for frame in self.source:
            yield cv2.cvtColor(frame, self.target_space)


class RandomColorspace(Processor):

    def __init__(self):
        self.colors = [
            cv2.COLOR_BGR2GRAY,
            cv2.COLOR_BGR2HLS,
            cv2.COLOR_BGR2HSV,
            # cv2.COLOR_BGR2LAB,
            # cv2.COLOR_BGR2LUV,
            # cv2.COLOR_BGR2Lab,
            # cv2.COLOR_BGR2Luv,
            # cv2.COLOR_BGR2RGB,
            # cv2.COLOR_BGR2XYZ,
            # cv2.COLOR_BGR2YCrCb,
            # cv2.COLOR_BGR2YUV,
        ]

    def iterate(self):
        for frame in self.source:
            yield cv2.cvtColor(frame, random.choice(self.colors))
