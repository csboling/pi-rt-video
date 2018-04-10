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
        # return (
        #     self.r(x, y, t),
        #     self.g(x, y, t),
        #     self.b(x, y, t),
        #     1.0,
        # )
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
        freqdiv = 2
        super().__init__( 
            r=lambda x, y, t: np.sin(
                np.exp(1.5*np.sin(t  / freqdiv)) / freqdiv
                *
                np.outer(x,y)*y
            ),
            g=lambda x, y, t: np.cos(
                np.exp(1.5*np.cos(t / freqdiv))*y  / freqdiv
            )*np.cos(np.outer(x,y)),
            b=lambda x, y, t: np.cos(
                np.exp(1.5*np.cos(t  / freqdiv)*np.sin(t  / freqdiv))  / freqdiv
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


class Checkerboard:   
    @params(offset=lambda t: (
        int(128 + 127*np.cos(2*np.pi*t / 8)),
        int(128 + 127*np.sin(3*np.pi*t / 8)),
    ))
    def __init__(self, offset):
        self.offset = offset

    def checks(self, offset, grid_num=8, grid_size=32):
        row_even = grid_num // 2 * [0, 1]
        row_odd = grid_num // 2 * [1, 0]
        Z = np.row_stack(grid_num // 2 * (row_even, row_odd)).astype(np.uint8)
        return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)
        
    def __call__(self, t):
        offset = self.offset(t)
        checks = self.checks(offset)
        return np.roll(checks, offset)


class Constant:
    def __init__(self):
        top = np.zeros((128, 256, 4))
        bottom = np.zeros((128, 256, 4))
        top[..., :] = [255, 255, 0, 255]
        bottom[..., :] = [0, 255, 0, 255]
        xs = WeirdSineColorMap()((256, 256), 0)
        import pdb; pdb.set_trace()
        self.constant = 255 * np.vstack([top, bottom])
    
    def __call__(self, t):
        return self.constant
