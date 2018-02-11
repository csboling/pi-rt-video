import numpy as np

from pipeline.processor.Processor import Processor


def rgb_to_frame(r, g, b):
    return  (
        np.array((r, g, b)) * 128 + 127
    ).transpose(2, 1, 0).astype(np.uint8)
    

class AnimatedColorMap(Processor):
    
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b

    def iterate(self):
        t = 0
        for frame in self.source:
            w, h = self.resolution
            x, y = (
                np.arange(-w//2, w//2)*4*2*np.pi/w, 
                np.arange(-h//2, h//2)*4*2*np.pi/h,
            )
            yield rgb_to_frame(
                self.r(x, y, t),
                self.g(x, y, t),
                self.b(x, y, t)
            )
            t = (t + 1 / self.framerate)
        

class FunkySineThing(AnimatedColorMap):
    def __init__(self):
        super().__init__(
            r=lambda x, y, t: np.sin(t*np.outer(x,y)*y),
            g=lambda x, y, t: np.cos(t*y)*np.cos(np.outer(x,y)),
            b=lambda x, y, t: np.cos(t*np.outer(x,y)+np.pi)
        )
