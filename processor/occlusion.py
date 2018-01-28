import numpy as np

from pipeline.animation.Animation import Animation
from pipeline.sprite.Sprite import Sprite
from pipeline.processor.Processor import Processor


class Occlusion(Processor):

    def __init__(self, sprite: Sprite, animation: Animation):
        self.sprite = sprite
        self.animation = animation

    def iterate(self):
        t = 0
        for frame in self.source:
            pos = self.animation.get_xy(frame, t)

            frame.setflags(write=1)
            self.sprite.draw(frame, pos, t)

            t += 1 / self.framerate
            yield frame
