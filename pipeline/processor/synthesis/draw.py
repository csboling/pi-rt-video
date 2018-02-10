from collections import Iterable
import itertools

import numpy as np
import pygame

from pipeline.processor.Processor import Processor
from pipeline.processor.pure import PureFunction
from pipeline.sprite.Sprite import Sprite


class Fill(PureFunction):
    def __init__(self, color):
        self.color = color

    def __call__(self, surface: pygame.Surface):
        surface.fill(self.color)
        return surface


def parse_color(color, gradient_points):
    if callable(color):
        return color
    if isinstance(color, Iterable):
        grad = Gradient(color, gradient_points)
        it = iter(grad)
        c = next(it)
        return lambda *args: next(it)

class Pen(Processor):
    def __init__(self, animation, color):
        self.animation = animation
        self.color = parse_color(color, 20)

    def iterate(self):
        t = 0
        prev_pos = None
        for surface in self.source:
            w, h = self.resolution
            pos = self.animation.get_xy((w, h), surface, t)
            color = self.color(pos, w, h, t)
            if prev_pos is not None:
                pygame.draw.aaline(surface, color, prev_pos, pos)

            prev_pos = pos
            t = (t + 1 / self.framerate)
            yield surface

class Circle(Sprite):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = parse_color(color)

    def draw(self, surface: pygame.Surface, pos, t):
        x, y = pos
        pygame.draw.circle(
            surface,
            self.color,
            (int(x), int(y)), self.radius
        )


class Gradient:
    def __init__(self, colors, points):
        self.colors = colors
        self.points = points

    def __iter__(self):
        return self.iterate()

    def iterate(self):
        it = itertools.cycle(self.colors)
        prev = None
        while True:
            curr = next(it)
            if prev is not None:
                gradient = np.vstack(
                    np.linspace(p, c, self.points) 
                    for p, c in zip(prev, curr)
                ).T
                yield from iter(gradient)
            prev = curr
