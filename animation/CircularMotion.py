import numpy as np

from pipeline.animation.Animation import Animation


class CircularMotion(Animation):

    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def get_xy(self, frame, t):
        return (
            self.center[0] + self.radius*np.cos(2*np.pi*(t % np.pi)),
            self.center[1] + self.radius*np.sin(2*np.pi*(t % np.pi)),
        )
