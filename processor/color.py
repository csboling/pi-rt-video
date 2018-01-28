import random

import cv2

from pipeline.processor.Processor import Processor


class GrayScaler(Processor):

    def iterate(self):
        for frame in self.source:
            yield cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


class RandomColorspace(Processor):

    def __init__(self):
        self.colors = [
            cv2.COLOR_BGR2BGRA,
            cv2.COLOR_BGR2GRAY,
            cv2.COLOR_BGR2HLS,
            cv2.COLOR_BGR2HLS_FULL,
            cv2.COLOR_BGR2HSV,
            cv2.COLOR_BGR2HSV_FULL,
            cv2.COLOR_BGR2LAB,
            cv2.COLOR_BGR2LUV,
            cv2.COLOR_BGR2Lab,
            cv2.COLOR_BGR2Luv,
            cv2.COLOR_BGR2RGB,
            cv2.COLOR_BGR2RGBA,
            cv2.COLOR_BGR2XYZ,
            cv2.COLOR_BGR2YCR_CB,
            cv2.COLOR_BGR2YCrCb,
            cv2.COLOR_BGR2YUV,
            cv2.COLOR_BGR2YUV_I420,
            cv2.COLOR_BGR2YUV_IYUV,
            cv2.COLOR_BGR2YUV_YV12,
        ]

    def iterate(self):
        for frame in self.source:
            yield cv2.cvtColor(frame, random.choice(self.colors))
