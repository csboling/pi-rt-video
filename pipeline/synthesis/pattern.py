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


class Checkerboard:
    def checks(self, grid_num=8, grid_size=32):
        row_even = grid_num // 2 * [0, 1]
        row_odd = grid_num // 2 * [1, 0]
        Z = np.row_stack(grid_num // 2 * (row_even, row_odd)).astype(np.uint8)
        return 255 * Z.repeat(grid_size, axis=0).repeat(grid_size, axis=1)
        
    def __call__(self, t):
        return self.checks()
            

# class Checkerboard:
#     @params(
#         bit_pattern=[
#             [1, 0, 1, 0],
#             [0, 1, 0, 1],
#             [1, 0, 1, 0],
#             [0, 1, 0, 1],
#         ],
#         offset=(0, 0),
#     )
#     def __init__(self, dims, bit_pattern, offset):
#         self.dims = dims
#         self.bit_pattern = bit_pattern
#         self.offset = offset

#     def __call__(self, t):
#         w, h = self.dims
#         bit_pattern = np.array(self.bit_pattern(t), dtype=np.bool)
#         offset = self.offset(t)

#         check_w = w // bit_pattern.shape[0]
#         check_h = h // bit_pattern.shape[1]
#         checks = np.zeros((*bit_pattern.shape, check_w, check_h, 4))
#         checks[bit_pattern] = (0, 0, 0, 4)
#         return np.roll(checks.reshape((w, h, 4)), offset)
