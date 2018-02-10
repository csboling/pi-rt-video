import random

import cv2

from pipeline.processor.pure import PureFunction, RandomPure


class ChangeColorspace(PureFunction):

    def __init__(self, target_space=cv2.COLOR_BGR2GRAY):
        self.target_space = target_space

    def __call__(self, frame):
        return cv2.cvtColor(frame, self.target_space)


class RandomColorspace(RandomPure):

    @staticmethod
    def functions():
        return [
            ChangeColorspace(mode)
            for mode in
            [
                cv2.COLOR_BGR2HLS,
                cv2.COLOR_BGR2HSV,
                cv2.COLOR_BGR2RGB,
                cv2.COLOR_BGR2XYZ,
            ]
        ]

    def __init__(self):
        super().__init__(self.functions())


class Threshold(PureFunction):

    def __init__(self, target_mode, threshold):
        self.target_mode = target_mode
        self.threshold = threshold

    def __call__(self, frame):
        return cv2.threshold(frame, *self.threshold, self.target_mode)[1]

class RandomThreshold(RandomPure):

    def __init__(self, threshold=(127, 255)):
        super().__init__([
            Threshold(mode, threshold)
            for mode in
            [
                cv2.THRESH_BINARY,
                cv2.THRESH_BINARY_INV,
                cv2.THRESH_TRUNC,
                cv2.THRESH_TOZERO,
                cv2.THRESH_TOZERO_INV,
            ]
        ])
