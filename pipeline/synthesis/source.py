import pygame
from pygame import (
    display,
    draw,
    surfarray,
)
from pygame.time import Clock


class VideoSynthesisSource:

    def __init__(self, resolution=None, framerate=30, fill=(0, 0, 0)):
        if resolution is None:
            pygame.init()
            info = display.Info()
            resolution = (info.current_w, info.current_h)
            print('detected resolution: {} x {}'.format(*resolution))

        self.surface = pygame.Surface(resolution)
        self.surface.fill(fill)
        self.framerate = framerate
        self.clock = Clock()

    @property
    def resolution(self):
        return self.surface.get_size()

    def __iter__(self):
        return self.iterate()

    def iterate(self):
        while True:
            yield self.surface
            self.clock.tick(self.framerate)
