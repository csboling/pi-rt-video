import numpy as np

from pipeline.sprite.Sprite import Sprite


class RandomSquare(Sprite):

    def __init__(self, dims):
        self.dims = dims

    def draw(self, frame, pos, t):
        x, y = pos
        w, h = self.dims

        frame[
            int(y):int(y)+h,
            int(x):int(x)+w,
        ] = np.random.randint(0, 255, size=(h, w, 3))
