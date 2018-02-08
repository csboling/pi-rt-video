import numpy as np

from pipeline.animation.Animation import Animation


class CircularMotion(Animation):

    def __init__(self, center, radius, velocity=1.):
        self.center = center
        self.radius = radius
        self.velocity = velocity

    def get_xy(self, res, frame, t):
        return (
            self.center[0] +
            self.radius * np.cos(
                2*np.pi*self.velocity*(t % 1.)
            ),
            self.center[1] +
            self.radius * np.sin(
                2*np.pi*self.velocity*(t % 1.)
            ),
        )
