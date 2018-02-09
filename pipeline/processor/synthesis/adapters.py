import numpy as np
from pygame import surfarray

from pipeline.processor.pure import PureFunction


class SurfarrayAdapter(PureFunction):
    def __call__(self, surface):
        return np.transpose(surfarray.pixels3d(surface), [1, 0, 2])

