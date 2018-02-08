import numpy as np
import pygame
from pygame import (
    display,
    draw,
    surfarray,
)
from pygame.time import Clock

from pipeline.animation import CircularMotion
from pipeline.Pipeline import Pipeline
from pipeline.playback import PlaybackSink
from pipeline.processor import (
    Occlusion,
    PureFunction,
    Reverb,
)
from pipeline.sprite import Sprite


class VideoSynthesisSource:

    def __init__(self, resolution=None, framerate=30):
        if resolution is None:
            pygame.init()
            info = display.Info()
            resolution = (info.current_w, info.current_h)

        self.surface = pygame.Surface(resolution)
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

class Fill(PureFunction):
    def __init__(self, color):
        self.color = color

    def __call__(self, surface):
        surface.fill(self.color)
        return surface

class SurfarrayAdapter(PureFunction):
    def __call__(self, surface):
        return np.transpose(surfarray.pixels3d(surface), [1, 0, 2])

class PygameCircle(Sprite):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def draw(self, surface, pos, t):
        x, y = pos
        draw.circle(
            surface,
            self.color,
            (int(x), int(y)), self.radius
        )


class VideoSynthesisPipeline(Pipeline):
    def __init__(self):
        source = VideoSynthesisSource()
        w, h = source.resolution
        super().__init__([
            source,
            Fill((0, 0, 0)),
            Occlusion(
                PygameCircle(10, (0, 255, 0)),
                CircularMotion((w // 2, h // 2), 50)
            ),
            SurfarrayAdapter(),
            Reverb(),
        ])

    def run(self):
        super().run(PlaybackSink)
