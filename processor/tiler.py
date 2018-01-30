from abc import abstractmethod
import random

import numpy as np

from pipeline.processor.Processor import Processor


class Tiler(Processor):
    def iterate(self):
        w, h = self.resolution
        for frame in self.source:
            out = np.zeros(frame.shape, dtype=frame.dtype)
            for (top, left), (bottom, right) in self.get_rects(w, h):
                out[top:bottom, left:right] = self.fill_region(
                    frame[top:bottom, left:right]
                )
            yield out

    @abstractmethod
    def get_rects(self, w, h):
        pass

    @abstractmethod
    def fill_region(self, region):
        pass


class RandomPureTiler(Tiler):
    def __init__(self, pures):
        self.pures = pures

    def get_rects(self, h, w):
        y = 0

        while y < h:
            x = 0
            x_stride = random.randint(8, 256)
            y_stride = random.randint(8, 256)
            while x < w:
                yield (
                    (y, x),
                    (y + y_stride, x + x_stride),
                )
                x += x_stride
            y += y_stride

    def fill_region(self, region):
        return random.choice(self.pures)(region)
