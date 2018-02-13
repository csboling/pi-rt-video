import pygame
from pygame.locals import *


from pipeline.playback.pygame import PygameSink


class OpenGLPygameSink(PygameSink):
    def initialize(self, res, flags=0):
        super().initialize(res, flags | DOUBLEBUF | OPENGL)

    def process(self, item):
        pygame.display.flip()


