import pygame

from pipeline.processor.pure import PureFunction
from pipeline.sprite.Sprite import Sprite


class Fill(PureFunction):
    def __init__(self, color):
        self.color = color

    def __call__(self, surface: pygame.Surface):
        surface.fill(self.color)
        return surface

class Circle(Sprite):
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def draw(self, surface: pygame.Surface, pos, t):
        x, y = pos
        pygame.draw.circle(
            surface,
            self.color,
            (int(x), int(y)), self.radius
        )


