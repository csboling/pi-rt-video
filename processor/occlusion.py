from abc import ABCMeta, abstractmethod

import numpy as np

from pipeline.processor.Processor import Processor


class Sprite(metaclass=ABCMeta):

    @abstractmethod
    def draw_scaled(self, frame, pos, dims, t):
        pass


class Occlusion(Processor):

    def __init__(self, sprite: Sprite, pos, dims):
        self.sprite = sprite
        self.pos = pos
        self.dims = dims

    def iterate(self):
        t = 0
        for frame in self.source:
            frame.setflags(write=1)
            self.sprite.draw_scaled(frame, self.pos, self.dims, t)
            t += 1 / self.framerate
            yield frame


class RandomSquare(Sprite):

    def draw_scaled(self, frame, pos, dims, t):
        x, y = pos
        w, h = dims

        frame[
            int(y):int(y)+h,
            int(x):int(x)+w,
        ] = np.random.randint(0, 255, size=(h, w, 3))
