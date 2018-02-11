import numpy as np

from pipeline.processor.Processor import Processor
from pipeline.utils import params


def rgb_to_frame(r, g, b):
    return  (
        np.array((r, g, b)) * 128 + 127
    ).transpose(2, 1, 0).astype(np.uint8)
    

class AnimatedColorMap:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def __call__(self, shape, t):
        w, h = shape
        x, y = (
            np.arange(-w//2, w//2)*4*2*np.pi/w, 
            np.arange(-h//2, h//2)*4*2*np.pi/h,
        )
        return rgb_to_frame(
            self.r(x, y, t),
            self.g(x, y, t),
            self.b(x, y, t)
        )


class UniformColorMap(AnimatedColorMap):
    @params(color=None)
    def __init__(self, color):
        self.color = color

    def __call__(self, shape, t):
        color = self.color(t)
        cells = np.zeros((*shape, 3))
        cells[..., :] = color
        return cells


class WeirdSineColorMap(AnimatedColorMap):
    def __init__(self):
        super().__init__( 
            r=lambda x, y, t: np.sin(
                np.exp(1.5*np.sin(t))
                *
                np.outer(x,y)*y
            ),
            g=lambda x, y, t: np.cos(
                np.exp(1.5*np.cos(t))*y
            )*np.cos(np.outer(x,y)),
            b=lambda x, y, t: np.cos(
                np.exp(1.5*np.cos(t)*np.sin(t))
                *
                np.outer(x,y)
                +
                np.pi
            )
        )


class AnimateMap(Processor):

    def __init__(self, color_map):
        self.color_map = color_map

    def iterate(self):
        t = 0
        for frame in self.source:
            w, h = self.resolution
            yield self.color_map((w, h), t)
            t += 1 / self.framerate

